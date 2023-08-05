extern crate rand;
#[macro_use(defer)]
extern crate scopeguard;

use pyo3::exceptions::PyRuntimeError;
use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::*;
use serde::ser::Error;
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::fmt;
use std::hash::Hash;
use std::hash::Hasher;
use std::ops::Deref;
use std::sync::atomic::AtomicBool;
use std::sync::atomic::AtomicUsize;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::thread;
use std::time::Duration;
use timely::WorkerConfig;

use timely::dataflow::operators::aggregation::*;
use timely::dataflow::operators::*;
use timely::dataflow::*;

pub(crate) mod webserver;

#[macro_use]
pub(crate) mod macros;

/// Represents a Python object flowing through a Timely dataflow.
///
/// A newtype for [`Py`]<[`PyAny`]> so we can
/// extend it with traits that Timely needs. See
/// <https://github.com/Ixrec/rust-orphan-rules> for why we need a
/// newtype and what they are.
#[derive(Clone, FromPyObject)]
struct TdPyAny(Py<PyAny>);

/// Rewrite some [`Py`] methods to automatically re-wrap as [`TdPyAny`].
impl TdPyAny {
    fn clone_ref(&self, py: Python) -> Self {
        self.0.clone_ref(py).into()
    }
}

/// Have access to all [`Py`] methods.
impl Deref for TdPyAny {
    type Target = Py<PyAny>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

/// Allows use in some Rust to Python conversions.
// I Don't really get the difference between ToPyObject and IntoPy
// yet.
impl ToPyObject for TdPyAny {
    fn to_object(&self, py: Python) -> Py<PyAny> {
        self.0.clone_ref(py)
    }
}

/// Allow passing to Python function calls without explicit
/// conversion.
impl IntoPy<PyObject> for TdPyAny {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.0
    }
}

/// Allow passing a reference to Python function calls without
/// explicit conversion.
impl IntoPy<PyObject> for &TdPyAny {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.0.clone_ref(_py)
    }
}

/// Conveniently re-wrap Python objects for use in Timely.
impl From<&PyAny> for TdPyAny {
    fn from(x: &PyAny) -> Self {
        Self(x.into())
    }
}

/// Conveniently re-wrap Python objects for use in Timely.
impl From<Py<PyAny>> for TdPyAny {
    fn from(x: Py<PyAny>) -> Self {
        Self(x)
    }
}

/// Allows you to debug print Python objects using their repr.
impl std::fmt::Debug for TdPyAny {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let s: PyResult<String> = Python::with_gil(|py| {
            let self_ = self.as_ref(py);
            let repr = self_.repr()?.to_str()?;
            Ok(String::from(repr))
        });
        f.write_str(&s.map_err(|_| std::fmt::Error {})?)
    }
}

/// Serialize Python objects flowing through Timely that cross
/// process bounds as pickled bytes.
impl serde::Serialize for TdPyAny {
    // We can't do better than isolating the Result<_, PyErr> part and
    // the explicitly converting.  1. `?` automatically trys to
    // convert using From<ReturnedError> for OuterError. But orphan
    // rule means we can't implement it since we don't own either py
    // or serde error types.  2. Using the newtype trick isn't worth
    // it, since you'd have to either wrap all the PyErr when they're
    // generated, or you implement From twice, once to get MyPyErr and
    // once to get serde::Err. And then you're calling .into()
    // explicitly since the last line isn't a `?` anyway.
    //
    // There's the separate problem if we could even implement the
    // Froms. We aren't allowed to "capture" generic types in an inner
    // `impl<S>` https://doc.rust-lang.org/error-index.html#E0401 and
    // we can't move them top-level since we don't know the concrete
    // type of S, and you're not allowed to have unconstrained generic
    // parameters https://doc.rust-lang.org/error-index.html#E0207 .
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let bytes: Result<Vec<u8>, PyErr> = Python::with_gil(|py| {
            let x = self.as_ref(py);
            let pickle = py.import("pickle")?;
            let bytes = pickle.call_method1("dumps", (x,))?.extract()?;
            Ok(bytes)
        });
        serializer.serialize_bytes(bytes.map_err(S::Error::custom)?.as_slice())
    }
}

struct PickleVisitor;
impl<'de> serde::de::Visitor<'de> for PickleVisitor {
    type Value = TdPyAny;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a pickled byte array")
    }

    fn visit_bytes<E>(self, bytes: &[u8]) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        let x: Result<TdPyAny, PyErr> = Python::with_gil(|py| {
            let pickle = py.import("pickle")?;
            let x = pickle.call_method1("loads", (bytes,))?.into();
            Ok(x)
        });
        x.map_err(E::custom)
    }
}

/// Deserialize Python objects flowing through Timely that cross
/// process bounds from pickled bytes.
impl<'de> serde::Deserialize<'de> for TdPyAny {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_bytes(PickleVisitor)
    }
}

/// Re-use Python's value semantics in Rust code.
///
/// Timely requires this whenever it internally "groups by".
impl PartialEq for TdPyAny {
    fn eq(&self, other: &Self) -> bool {
        use pyo3::class::basic::CompareOp;

        Python::with_gil(|py| {
            // Don't use Py.eq or PyAny.eq since it only checks
            // pointer identity.
            let self_ = self.as_ref(py);
            let other = other.as_ref(py);
            with_traceback!(py, self_.rich_compare(other, CompareOp::Eq)?.is_true())
        })
    }
}

/// Possibly a footgun.
///
/// Timely internally stores values in [`HashMap`] which require keys
/// to be [`Eq`] so we have to implement this (or somehow write our
/// own hash maps that could ignore this), but we can't actually
/// guarantee that any Python type will actually have a correct sense
/// of total equality. It's possible broken `__eq__` implementations
/// will cause mysterious behavior.
impl Eq for TdPyAny {}

/// Custom hashing semantics.
///
/// We can't use Python's `hash` because it is not consistent across
/// processes. Instead we have our own "exchange hash". See module
/// `bytewax.exhash` for definitions and how to implement for your own
/// types.
///
/// Timely requires this whenever it exchanges or accumulates data in
/// hash maps.
impl Hash for TdPyAny {
    fn hash<H: Hasher>(&self, state: &mut H) {
        Python::with_gil(|py| {
            with_traceback!(py, {
                let exhash = PyModule::import(py, "bytewax.exhash")?;
                let digest = exhash
                    .getattr("exhash")?
                    .call1((self,))?
                    .call_method0("digest")?
                    .extract()?;
                state.write(digest);
                PyResult::Ok(())
            });
        });
    }
}

/// A Python iterator that only gets the GIL when calling .next() and
/// automatically wraps in [`TdPyAny`].
///
/// Otherwise the GIL would be held for the entire life of the iterator.
#[derive(Clone)]
struct TdPyIterator(Py<PyIterator>);

/// Have PyO3 do type checking to ensure we only make from iterable
/// objects.
impl<'source> FromPyObject<'source> for TdPyIterator {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        Ok(ob.iter()?.into())
    }
}

/// Conveniently re-wrap PyO3 objects.
impl From<&PyIterator> for TdPyIterator {
    fn from(x: &PyIterator) -> Self {
        Self(x.into())
    }
}

/// Restricted Rust interface that only makes sense for iterators.
///
/// Just pass through to [`Py`].
///
/// This is mostly empty because [`Iterator`] does the heavy lifting
/// for defining the iterator API.
impl TdPyIterator {
    fn clone_ref(&self, py: Python) -> Self {
        Self(self.0.clone_ref(py))
    }
}

impl Iterator for TdPyIterator {
    type Item = TdPyAny;

    fn next(&mut self) -> Option<Self::Item> {
        Python::with_gil(|py| {
            let mut iter = self.0.as_ref(py);
            iter.next().map(|r| with_traceback!(py, r).into())
        })
    }
}

/// A Python object that is callable.
struct TdPyCallable(Py<PyAny>);

/// Have PyO3 do type checking to ensure we only make from callable
/// objects.
impl<'source> FromPyObject<'source> for TdPyCallable {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        if ob.is_callable() {
            Ok(Self(ob.into()))
        } else {
            let msg = if let Ok(type_name) = ob.get_type().name() {
                format!("'{type_name}' object is not callable")
            } else {
                "object is not callable".to_string()
            };
            Err(PyTypeError::new_err(msg))
        }
    }
}

/// Restricted Rust interface that only makes sense on callable
/// objects.
///
/// Just pass through to [`Py`].
impl TdPyCallable {
    fn clone_ref(&self, py: Python) -> Self {
        Self(self.0.clone_ref(py))
    }

    fn call0(&self, py: Python) -> PyResult<Py<PyAny>> {
        self.0.call0(py)
    }

    fn call1(&self, py: Python, args: impl IntoPy<Py<PyTuple>>) -> PyResult<Py<PyAny>> {
        self.0.call1(py, args)
    }
}

/// Styles of input for a Bytewax dataflow. Built as part of
/// calling [`Dataflow::new`].
///
/// PyO3 will automatically generate one of these given the Python
/// object is an iterator or a callable.
#[derive(FromPyObject)]
enum Input {
    /// A dataflow that uses a Singleton as its input will receive
    /// data from a single Python `Iterator[Tuple[int, Any]]` where
    /// the `int` is the timestamp for that element and `Any` is the
    /// data element itself.
    ///
    /// Only worker `0` will run this iterator and then we'll
    /// immediately distribute the items to every worker randomly.
    // Have PyO3 ignore that this is a named field and just try to
    // make a TdPyIterator out of the argument it's trying to turn
    // into this.
    #[pyo3(transparent)]
    Singleton { worker_0s_input: TdPyIterator },

    /// A dataflow that uses a Partitioned input will have each worker
    /// generate its own input from a builder function `def
    /// build(worker_index: int, total_workers: int) ->
    /// Iterable[Tuple[int, Any]]` where `int` is the timestamp for
    /// that element and `Any` is the data element itself.
    ///
    /// Each worker will call this function independently so they
    /// should return disjoint data.
    #[pyo3(transparent)]
    Partitioned {
        per_worker_input_builder: TdPyCallable,
    },
}

/// The definition of one step in a Bytewax dataflow graph.
///
/// This isn't actually used during execution, just during building.
///
/// See
/// <https://docs.rs/timely/latest/timely/dataflow/operators/index.html>
/// for Timely's operators. We try to keep the same semantics here.
enum Step {
    Map {
        mapper: TdPyCallable,
    },
    FlatMap {
        mapper: TdPyCallable,
    },
    Filter {
        predicate: TdPyCallable,
    },
    Inspect {
        inspector: TdPyCallable,
    },
    InspectEpoch {
        inspector: TdPyCallable,
    },
    Reduce {
        reducer: TdPyCallable,
        is_complete: TdPyCallable,
    },
    ReduceEpoch {
        reducer: TdPyCallable,
    },
    ReduceEpochLocal {
        reducer: TdPyCallable,
    },
    MapStateful {
        builder: TdPyCallable,
        mapper: TdPyCallable,
    },
    Capture {
        captor: TdPyCallable,
    },
}

/// The definition of Bytewax dataflow graph.
///
/// This isn't actually used during execution, just during building.
///
/// TODO: Right now this is just a linear dataflow only.
#[pyclass]
struct Dataflow {
    input: Input,
    steps: Vec<Step>,
}

#[pymethods]
impl Dataflow {
    #[new]
    fn new(input: Input) -> Self {
        Self {
            input: input,
            steps: Vec::new(),
        }
    }

    /// **Map** is a one-to-one transformation of items.
    ///
    /// It calls a function `mapper(item: Any) => updated_item: Any`
    /// on each item.
    ///
    /// It emits each transformed item downstream.
    fn map(&mut self, mapper: TdPyCallable) {
        self.steps.push(Step::Map { mapper });
    }

    /// **Flat Map** is a one-to-many transformation of items.
    ///
    /// It calls a function `mapper(item: Any) => emit: Iterable[Any]`
    /// on each item.
    ///
    /// It emits each element in the downstream iterator individually.
    fn flat_map(&mut self, mapper: TdPyCallable) {
        self.steps.push(Step::FlatMap { mapper });
    }

    /// **Filter** selectively keeps only some items.
    ///
    /// It calls a function `predicate(item: Any) => should_emit:
    /// bool` on each item.
    ///
    /// It emits the item downstream unmodified if the predicate
    /// returns `True`.
    fn filter(&mut self, predicate: TdPyCallable) {
        self.steps.push(Step::Filter { predicate });
    }

    /// **Inspect** allows you to observe, but not modify, items.
    ///
    /// It calls a function `inspector(item: Any) => None` on each
    /// item.
    ///
    /// The return value is ignored; it emits items downstream
    /// unmodified.
    fn inspect(&mut self, inspector: TdPyCallable) {
        self.steps.push(Step::Inspect { inspector });
    }

    /// **Inspect Epoch** allows you to observe, but not modify, items
    /// and their epochs.
    ///
    /// It calls a function `inspector(epoch: int, item: Any) => None`
    /// on each item with its epoch.
    ///
    /// The return value is ignored; it emits items downstream
    /// unmodified.
    fn inspect_epoch(&mut self, inspector: TdPyCallable) {
        self.steps.push(Step::InspectEpoch { inspector });
    }

    /// **Reduce** lets you combine items for a key into an
    /// aggregator in epoch order.
    ///
    /// Since this is a stateful operator, it requires the the input
    /// stream has items that are `(key, value)` tuples so we can
    /// ensure that all relevant values are routed to the relevant
    /// aggregator.
    ///
    /// It calls two functions:
    ///
    /// - A `reducer(aggregator: Any, value: Any) =>
    /// updated_aggregator: Any` which combines two values. The
    /// aggregator is initially the first value seen for a key. Values
    /// will be passed in epoch order, but no order is defined within
    /// an epoch.
    ///
    /// - An `is_complete(updated_aggregator: Any) => should_emit: bool` which
    /// returns true if the most recent `(key, aggregator)` should be
    /// emitted downstream and the aggregator for that key
    /// forgotten. If there was only a single value for a key, it is
    /// passed in as the aggregator here.
    ///
    /// It emits `(key, aggregator)` tuples downstream when you tell
    /// it to.
    fn reduce(&mut self, reducer: TdPyCallable, is_complete: TdPyCallable) {
        self.steps.push(Step::Reduce {
            reducer,
            is_complete,
        });
    }

    /// **Reduce Epoch** lets you combine all items for a key within
    /// an epoch into an aggregator.
    ///
    /// This is like `reduce` but marks the aggregator as complete
    /// automatically at the end of each epoch.
    ///
    /// Since this is a stateful operator, it requires the the input
    /// stream has items that are `(key, value)` tuples so we can
    /// ensure that all relevant values are routed to the relevant
    /// aggregator.
    ///
    /// It calls a function `reducer(aggregator: Any, value: Any) =>
    /// updated_aggregator: Any` which combines two values. The
    /// aggregator is initially the first value seen for a key. Values
    /// will be passed in arbitrary order.
    ///
    /// It emits `(key, aggregator)` tuples downstream at the end of
    /// each epoch.
    fn reduce_epoch(&mut self, reducer: TdPyCallable) {
        self.steps.push(Step::ReduceEpoch { reducer });
    }

    /// **Reduce Epoch Local** lets you combine all items for a key
    /// within an epoch _on a single worker._
    ///
    /// It is exactly like `reduce_epoch` but does no internal
    /// exchange between workers. You'll probably should use that
    /// instead unless you are using this as a network-overhead
    /// optimization.
    fn reduce_epoch_local(&mut self, reducer: TdPyCallable) {
        self.steps.push(Step::ReduceEpochLocal { reducer });
    }

    /// **Stateful Map** is a one-to-one transformation of values in
    /// `(key, value)` pairs, but allows you to reference a persistent
    /// state for each key when doing the transformation.
    ///
    /// Since this is a stateful operator, it requires the the input
    /// stream has items that are `(key, value)` tuples so we can
    /// ensure that all relevant values are routed to the relevant
    /// state.
    ///
    /// It calls two functions:
    ///
    /// - A `builder() => new_state: Any` which returns a new state
    /// and will be called whenever a new key is encountered.
    ///
    /// - A `mapper(state: Any, value: Any) => (updated_state: Any,
    /// updated_value: Any)` which transforms values. Values will be
    /// passed in epoch order, but no order is defined within an
    /// epoch. If the updated state is `None`, the state will be
    /// forgotten.
    ///
    /// It emits a `(key, updated_value)` tuple downstream for each
    /// input item.
    fn stateful_map(&mut self, builder: TdPyCallable, mapper: TdPyCallable) {
        self.steps.push(Step::MapStateful { builder, mapper });
    }

    /// **Capture** records all `(epoch, item)` pairs that pass by.
    ///
    /// All data on all workers will be captured.
    ///
    /// It calls a function `captor(epoch_item: tuple[int, Any]) =>
    /// None` on each item of data. There are no ordering guarantees.
    fn capture(&mut self, captor: TdPyCallable) {
        self.steps.push(Step::Capture { captor });
    }
}

// These are all shims which map the Timely Rust API into equivalent
// calls to Python functions through PyO3.

fn build(builder: &TdPyCallable) -> TdPyAny {
    Python::with_gil(|py| with_traceback!(py, builder.call0(py)).into())
}

fn map(mapper: &TdPyCallable, item: TdPyAny) -> TdPyAny {
    Python::with_gil(|py| with_traceback!(py, mapper.call1(py, (item,))).into())
}

fn flat_map(mapper: &TdPyCallable, item: TdPyAny) -> TdPyIterator {
    Python::with_gil(|py| with_traceback!(py, mapper.call1(py, (item,))?.extract(py)))
}

fn filter(predicate: &TdPyCallable, item: &TdPyAny) -> bool {
    Python::with_gil(|py| with_traceback!(py, predicate.call1(py, (item,))?.extract(py)))
}

fn inspect(inspector: &TdPyCallable, item: &TdPyAny) {
    Python::with_gil(|py| {
        with_traceback!(py, inspector.call1(py, (item,)));
    });
}

fn inspect_epoch(inspector: &TdPyCallable, epoch: &u64, item: &TdPyAny) {
    Python::with_gil(|py| {
        with_traceback!(py, inspector.call1(py, (*epoch, item)));
    });
}

/// Turn a Python 2-tuple into a Rust 2-tuple.
fn lift_2tuple(key_value_pytuple: TdPyAny) -> (TdPyAny, TdPyAny) {
    Python::with_gil(|py| with_traceback!(py, key_value_pytuple.as_ref(py).extract()))
}

/// Turn a Rust 2-tuple into a Python 2-tuple.
fn wrap_2tuple(key_value: (TdPyAny, TdPyAny)) -> TdPyAny {
    Python::with_gil(|py| key_value.to_object(py).into())
}

fn hash(key: &TdPyAny) -> u64 {
    let mut hasher = DefaultHasher::new();
    key.hash(&mut hasher);
    hasher.finish()
}

fn reduce(
    reducer: &TdPyCallable,
    is_complete: &TdPyCallable,
    aggregator: &mut Option<TdPyAny>,
    key: &TdPyAny,
    value: TdPyAny,
) -> (bool, impl IntoIterator<Item = TdPyAny>) {
    Python::with_gil(|py| {
        let updated_aggregator = match aggregator {
            Some(aggregator) => {
                with_traceback!(py, reducer.call1(py, (aggregator.clone_ref(py), value))).into()
            }
            None => value,
        };
        let should_emit_and_discard_aggregator: bool = with_traceback!(
            py,
            is_complete
                .call1(py, (updated_aggregator.clone_ref(py),))?
                .extract(py)
        );

        *aggregator = Some(updated_aggregator.clone_ref(py));

        if should_emit_and_discard_aggregator {
            let emit = (key.clone_ref(py), updated_aggregator).to_object(py).into();
            (true, Some(emit))
        } else {
            (false, None)
        }
    })
}

fn reduce_epoch(
    reducer: &TdPyCallable,
    aggregator: &mut Option<TdPyAny>,
    _key: &TdPyAny,
    value: TdPyAny,
) {
    Python::with_gil(|py| {
        let updated_aggregator = match aggregator {
            Some(aggregator) => {
                with_traceback!(py, reducer.call1(py, (aggregator.clone_ref(py), value))).into()
            }
            None => value,
        };
        *aggregator = Some(updated_aggregator);
    });
}

fn reduce_epoch_local(
    reducer: &TdPyCallable,
    aggregators: &mut HashMap<TdPyAny, TdPyAny>,
    all_key_value_in_epoch: &Vec<(TdPyAny, TdPyAny)>,
) {
    Python::with_gil(|py| {
        for (key, value) in all_key_value_in_epoch {
            aggregators
                .entry(key.clone_ref(py))
                .and_modify(|aggregator| {
                    *aggregator =
                        with_traceback!(py, reducer.call1(py, (aggregator.clone_ref(py), value)))
                            .into()
                })
                .or_insert(value.clone_ref(py));
        }
    });
}

fn stateful_map(
    mapper: &TdPyCallable,
    state: &mut TdPyAny,
    key: &TdPyAny,
    value: TdPyAny,
) -> (bool, impl IntoIterator<Item = TdPyAny>) {
    Python::with_gil(|py| {
        let (updated_state, emit_value): (TdPyAny, TdPyAny) = with_traceback!(
            py,
            mapper.call1(py, (state.clone_ref(py), value))?.extract(py)
        );

        *state = updated_state;

        let discard_state = Python::with_gil(|py| state.is_none(py));
        let emit = (key, emit_value).to_object(py).into();
        (discard_state, std::iter::once(emit))
    })
}

fn capture(captor: &TdPyCallable, epoch: &u64, item: &TdPyAny) {
    Python::with_gil(|py| with_traceback!(py, captor.call1(py, ((*epoch, item.clone_ref(py)),))));
}

// End of shim functions.

/// Encapsulates the process of pulling data out of the input Python
/// iterator and feeding it into Timely.
///
/// This will be called in the worker's "main" loop to feed data in.
struct Pump {
    pull_from_pyiter: TdPyIterator,
    pyiter_is_empty: bool,
    push_to_timely: InputHandle<u64, TdPyAny>,
}

impl Pump {
    fn new(pull_from_pyiter: TdPyIterator, push_to_timely: InputHandle<u64, TdPyAny>) -> Self {
        Self {
            pull_from_pyiter,
            pyiter_is_empty: false,
            push_to_timely,
        }
    }

    /// Take a single data element and timestamp and feed it into the
    /// dataflow.
    fn pump(&mut self) {
        Python::with_gil(|py| {
            let mut pull_from_pyiter = self.pull_from_pyiter.0.as_ref(py);
            if let Some(epoch_item_pytuple) = pull_from_pyiter.next() {
                let (epoch, item) = with_traceback!(py, epoch_item_pytuple?.extract());
                self.push_to_timely.advance_to(epoch);
                self.push_to_timely.send(item);
            } else {
                self.pyiter_is_empty = true;
            }
        });
    }

    fn input_remains(&self) -> bool {
        !self.pyiter_is_empty
    }
}

fn build_dataflow<A>(
    timely_worker: &mut timely::worker::Worker<A>,
    py: Python,
    dataflow: &Dataflow,
) -> (Option<Pump>, ProbeHandle<u64>)
where
    A: timely::communication::Allocate,
{
    let this_worker_index = timely_worker.index();
    let total_worker_count = timely_worker.peers();
    timely_worker.dataflow(|scope| {
        let mut timely_input = InputHandle::new();
        let mut end_of_steps_probe = ProbeHandle::new();
        let mut stream = timely_input.to_stream(scope);

        if let Input::Singleton { .. } = dataflow.input {
            stream = stream.exchange(|_| rand::random());
        }

        let steps = &dataflow.steps;
        for step in steps {
            match step {
                Step::Map { mapper } => {
                    // All these closure lifetimes are static, so tell
                    // Python's GC that there's another pointer to the
                    // mapping function that's going to hang around
                    // for a while when it's moved into the closure.
                    let mapper = mapper.clone_ref(py);
                    stream = stream.map(move |item| map(&mapper, item));
                }
                Step::FlatMap { mapper } => {
                    let mapper = mapper.clone_ref(py);
                    stream = stream.flat_map(move |item| flat_map(&mapper, item));
                }
                Step::Filter { predicate } => {
                    let predicate = predicate.clone_ref(py);
                    stream = stream.filter(move |item| filter(&predicate, item));
                }
                Step::Inspect { inspector } => {
                    let inspector = inspector.clone_ref(py);
                    stream = stream.inspect(move |item| inspect(&inspector, item));
                }
                Step::InspectEpoch { inspector } => {
                    let inspector = inspector.clone_ref(py);
                    stream = stream
                        .inspect_time(move |epoch, item| inspect_epoch(&inspector, epoch, item));
                }
                Step::Reduce {
                    reducer,
                    is_complete,
                } => {
                    let reducer = reducer.clone_ref(py);
                    let is_complete = is_complete.clone_ref(py);
                    stream = stream.map(lift_2tuple).state_machine(
                        move |key, value, aggregator: &mut Option<TdPyAny>| {
                            reduce(&reducer, &is_complete, aggregator, key, value)
                        },
                        hash,
                    );
                }
                Step::ReduceEpoch { reducer } => {
                    let reducer = reducer.clone_ref(py);
                    stream = stream.map(lift_2tuple).aggregate(
                        move |key, value, aggregator: &mut Option<TdPyAny>| {
                            reduce_epoch(&reducer, aggregator, key, value);
                        },
                        move |key, aggregator: Option<TdPyAny>| {
                            // Aggregator will only exist for keys
                            // that exist, so it will have been filled
                            // into Some(value) above.
                            wrap_2tuple((key, aggregator.unwrap()))
                        },
                        hash,
                    );
                }
                Step::ReduceEpochLocal { reducer } => {
                    let reducer = reducer.clone_ref(py);
                    stream = stream
                        .map(lift_2tuple)
                        .accumulate(
                            HashMap::new(),
                            move |aggregators, all_key_value_in_epoch| {
                                reduce_epoch_local(&reducer, aggregators, &all_key_value_in_epoch);
                            },
                        )
                        .flat_map(|aggregators| aggregators.into_iter().map(wrap_2tuple));
                }
                Step::MapStateful { builder, mapper } => {
                    let builder = builder.clone_ref(py);
                    let mapper = mapper.clone_ref(py);
                    stream = stream.map(lift_2tuple).state_machine(
                        move |key, value, maybe_uninit_state: &mut Option<TdPyAny>| {
                            let state = maybe_uninit_state.get_or_insert_with(|| build(&builder));
                            stateful_map(&mapper, state, key, value)
                        },
                        hash,
                    );
                }
                Step::Capture { captor } => {
                    let captor = captor.clone_ref(py);
                    // TODO: Figure out which worker is running
                    // build_and_run() and make sure we exchange to
                    // that one so the "controlling process" will be
                    // the one with the output data. Returning 0 here
                    // doesn't guaratnee worker 0.
                    stream = stream
                        .exchange(|_| 0)
                        .inspect_time(move |epoch, item| capture(&captor, epoch, item));
                }
            }
        }
        stream.probe_with(&mut end_of_steps_probe);

        let pump: Option<Pump> = match &dataflow.input {
            Input::Singleton { worker_0s_input } => {
                if this_worker_index == 0 {
                    let worker_0s_input = worker_0s_input.clone_ref(py);
                    Some(Pump::new(worker_0s_input, timely_input))
                } else {
                    None
                }
            }
            Input::Partitioned {
                per_worker_input_builder,
            } => {
                let this_builders_input_iter = per_worker_input_builder
                    .call1(py, (this_worker_index, total_worker_count))
                    .unwrap()
                    .extract(py)
                    .unwrap();
                Some(Pump::new(this_builders_input_iter, timely_input))
            }
        };

        (pump, end_of_steps_probe)
    })
}

/// "Main loop" of a Timely worker thread.
///
/// 1. Pump [`Pump`]s (get input data from Python into Timely).
///
/// 2. Dispose of empty [`Pump`]s and Probes which indicate there's no
/// data left to process in that dataflow.
///
/// 3. Call [timely::worker::Worker::step] to tell Timely to do
/// whatever work it can.
fn worker_main<A>(
    mut pumps_with_input_remaining: Vec<Pump>,
    mut probes_with_timestamps_inflight: Vec<ProbeHandle<u64>>,
    interrupt_flag: &Arc<AtomicBool>,
    worker: &mut timely::worker::Worker<A>,
) where
    A: timely::communication::Allocate,
{
    while (!pumps_with_input_remaining.is_empty() || !probes_with_timestamps_inflight.is_empty())
        && !interrupt_flag.load(Ordering::Relaxed)
    {
        if !pumps_with_input_remaining.is_empty() {
            let mut updated_pumps = Vec::new();
            for mut pump in pumps_with_input_remaining.into_iter() {
                pump.pump();
                if pump.input_remains() {
                    updated_pumps.push(pump);
                }
            }
            pumps_with_input_remaining = updated_pumps;
        }
        if !probes_with_timestamps_inflight.is_empty() {
            let mut updated_probes = Vec::new();
            for probe in probes_with_timestamps_inflight.into_iter() {
                if !probe.done() {
                    updated_probes.push(probe);
                }
            }
            probes_with_timestamps_inflight = updated_probes;
        }

        worker.step();
    }
}

/// Main Bytewax class that handles defining and executing
/// dataflows.
///
/// Create a new dataflow for a stream of input with
/// [`Dataflow`], add steps to it using the methods within
/// (e.g. `map`), then build and run it using [`build_and_run`].
#[pyclass]
struct Executor {
    dataflows: Vec<Py<Dataflow>>,
}

#[pymethods]
impl Executor {
    #[new]
    fn new() -> Self {
        Executor {
            dataflows: Vec::new(),
        }
    }

    /// Create a new empty dataflow blueprint that you can add steps
    /// to.
    #[pyo3(name = "Dataflow")] // Cuz it's sort of the class constructor.
    fn dataflow(&mut self, py: Python, input: Input) -> PyResult<Py<Dataflow>> {
        // For some reason we can only return Rust-owned objects in
        // #[new], which is totally unlike the API of PyList::new(py,
        // ...) which returns something already on the Python
        // heap. This means we need to send it to Python right away to
        // have a Py pointer we can clone into the vec and return now.
        let dataflow = Py::new(py, Dataflow::new(input))?;
        self.dataflows.push(dataflow.clone());
        Ok(dataflow)
    }

    /// Build all of the previously-defined dataflow blueprints and
    /// run them.
    ///
    ///
    /// # Arguments
    ///
    /// * `threads` - The number of per-process worker threads to use.
    /// * `processes` - The number of processes that were started.
    /// * `process` - Which process number this instance represents.
    /// * `processes` - The total number of processes.
    /// * `addresses` - An optional list of host/port addresses for other Bytewax workers.
    #[args(threads = 1, processes = 0, process = 0, addresses = "None")]
    fn build_and_run(
        self_: Py<Self>,
        py: Python,
        threads: usize,
        process: usize,
        processes: usize,
        addresses: Option<Vec<String>>,
    ) -> PyResult<()> {
        py.allow_threads(move || {
            let (builders, other) = match processes {
                0 => timely::CommunicationConfig::Process(threads),
                _ => {
                    let addresses = addresses.unwrap_or_else(|| {
                        let mut local_addrs = Vec::new();
                        for index in 0..processes {
                            local_addrs.push(format!("localhost:{}", 2101 + index));
                        }
                        local_addrs
                    });
                    timely::CommunicationConfig::Cluster {
                        threads,
                        process,
                        addresses,
                        report: false,
                        log_fn: Box::new(|_| None),
                    }
                }
            }
            .try_build()
            .map_err(PyRuntimeError::new_err)?;

            let should_shutdown = Arc::new(AtomicBool::new(false));
            let should_shutdown_w = should_shutdown.clone();
            let should_shutdown_p = should_shutdown.clone();
            // We can drop these if we want to use nightly
            // Thread::is_running
            // https://github.com/rust-lang/rust/issues/90470
            let shutdown_worker_count = Arc::new(AtomicUsize::new(0));
            let shutdown_worker_count_w = shutdown_worker_count.clone();
            let shutdown_worker_count_p = shutdown_worker_count.clone();

            // Panic hook is per-process, so this isn't perfect as you
            // can't call Executor.build_and_run() concurrently.
            let default_hook = std::panic::take_hook();
            std::panic::set_hook(Box::new(move |info| {
                should_shutdown_p.store(true, Ordering::Relaxed);
                shutdown_worker_count_p.fetch_add(1, Ordering::Relaxed);

                if let Some(pyerr) = info.payload().downcast_ref::<PyErr>() {
                    Python::with_gil(|py| pyerr.print(py));
                } else {
                    default_hook(info);
                }
            }));
            // Don't chain panic hooks if we run multiple
            // dataflows. Really this is all a hack because the panic
            // hook is global state. There's some talk of per-thread
            // panic hooks which would help
            // here. https://internals.rust-lang.org/t/pre-rfc-should-std-set-hook-have-a-per-thread-version/9518/3
            defer! {
                let _ = std::panic::take_hook();
            }

            let guards = timely::execute::execute_from(
                builders,
                other,
                WorkerConfig::default(),
                move |worker| {
                    let mut all_pumps = Vec::new();
                    let mut all_probes = Vec::new();

                    Python::with_gil(|py| {
                        // These borrows should be safe because nobody else
                        // will have a mut ref. Although they might have
                        // shared refs.
                        let self_ = self_.as_ref(py).borrow();
                        for dataflow in &self_.dataflows {
                            let dataflow = dataflow.as_ref(py).borrow();
                            let (pump, probe) = build_dataflow(worker, py, &dataflow);
                            all_pumps.extend(pump);
                            all_probes.push(probe);
                        }
                    });

                    worker_main(all_pumps, all_probes, &should_shutdown_w, worker);

                    // Timely spins until all dataflows have been
                    // explicitly dropped. Drop everything now to
                    // allow graceful shutdown.
                    for dataflow_id in worker.installed_dataflows() {
                        worker.drop_dataflow(dataflow_id);
                    }
                    shutdown_worker_count_w.fetch_add(1, Ordering::Relaxed);
                },
            )
            .map_err(PyRuntimeError::new_err)?;

            // Recreating what Python does in Thread.join() to "block"
            // but also check interrupt handlers.
            // https://github.com/python/cpython/blob/204946986feee7bc80b233350377d24d20fcb1b8/Modules/_threadmodule.c#L81
            let workers_in_proc_count = guards.guards().len();
            while shutdown_worker_count.load(Ordering::Relaxed) < workers_in_proc_count {
                thread::sleep(Duration::from_millis(1));
                Python::with_gil(|py| Python::check_signals(py)).map_err(|err| {
                    should_shutdown.store(true, Ordering::Relaxed);
                    err
                })?;
            }
            for maybe_worker_panic in guards.join() {
                // See if we can PR Timely to not cast panic info to
                // String. Then we could re-raise Python exception in
                // main thread and not need to print in
                // panic::set_hook above, although we still need it to
                // tell the other workers to do graceful shutdown.
                maybe_worker_panic.map_err(|_| {
                    PyRuntimeError::new_err("Worker thread died; look for errors above")
                })?;
            }

            Ok(())
        })
    }
}

#[pyfunction]
fn sleep_keep_gil(_py: Python, secs: u64) -> () {
    thread::sleep(Duration::from_secs(secs));
}

#[pyfunction]
fn sleep_release_gil(_py: Python, secs: u64) -> () {
    _py.allow_threads(|| {
        thread::sleep(Duration::from_secs(secs));
    });
}

#[pymodule]
#[pyo3(name = "bytewax")]
fn mod_tiny_dancer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Dataflow>()?;
    m.add_class::<Executor>()?;

    m.add_function(wrap_pyfunction!(sleep_keep_gil, m)?)?;
    m.add_function(wrap_pyfunction!(sleep_release_gil, m)?)?;

    Ok(())
}
