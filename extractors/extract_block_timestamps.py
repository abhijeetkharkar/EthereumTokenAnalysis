import urllib.request
import json
from config_files import config
import pickle
from datetime import datetime
import multiprocessing


def get_block_details(block_tuple):
    print("Block Tuple: (", multiprocessing.current_process().name, "):", block_tuple)
    earliest_block = block_tuple[0]
    current_block = earliest_block
    latest_block = block_tuple[1]

    block_timestamps_map = dict()

    with open('json_requests/get_block_details.json') as json_data:
        data = json.load(json_data)

    # for block_number in range(earliest_block, latest_block+1):
    while current_block is not latest_block:
        req = urllib.request.Request(config.CONFIGURATION['DEFAULT']['GETH_URL'])
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        data["params"][0] = hex(current_block)

        response_str = "**Default**"

        try:
            response = urllib.request.urlopen(req, json.dumps(data).encode("utf-8"))

            # print("Response:", response.read())

            # block_details = json.loads(response.read().strip())["result"]
            # block_timestamps_map[current_block] = datetime.fromtimestamp(int(block_details["timestamp"].strip())/1000.0)

            response_str = str(response.read())
            # print(response_str)
            # timestamp = int(response_str[response_str.find('"timestamp"') + 13:][0:response_str[response_str.find('"timestamp"') + 13:].find('"')], 16)
            # block_timestamps_map[current_block] = datetime.fromtimestamp(timestamp / 1000.0)
            block_timestamps_map[current_block] = response_str

            current_block += 1
            if current_block % 100000 == 0:
                print("Progress (", multiprocessing.current_process().name, "):", round((current_block - earliest_block) / (latest_block - earliest_block) * 100, 4))
        except ValueError:
            print("Erroneous Block:", current_block)
            block_timestamps_map[current_block] = response_str
        except ConnectionError:
            pass

    return block_timestamps_map
