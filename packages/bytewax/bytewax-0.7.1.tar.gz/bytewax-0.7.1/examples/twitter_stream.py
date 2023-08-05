import json
import operator
import time
from collections import defaultdict

import bytewax
from bytewax import inp

from utils import twitter


def decode(x):
    try:
        return [json.loads(x)]
    except ValueError:
        return []  # Ignore errors. This will skip because in flat_map.


def coin_name(data_dict):
    # Get all of the mentioned hashtags.
    return [x["tag"] for x in data_dict["matching_rules"]]


def initial_count(coin):
    return coin, 1


ec = bytewax.Executor()
flow = ec.Dataflow(inp.tumbling_epoch(2.0, twitter.get_stream()))
# "event_json"
flow.flat_map(decode)
# {event_dict}
flow.flat_map(coin_name)
# "coin"
flow.map(initial_count)
# ("coin", 1)
flow.reduce_epoch(operator.add)
# ("coin", count)
flow.inspect(print)


if __name__ == "__main__":
    ec.build_and_run()
