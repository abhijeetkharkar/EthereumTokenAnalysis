import urllib.request
import json
from config_files import config
from datetime import datetime
import multiprocessing
import contextlib
import requests
import time
import sys


def get_block_details(block_tuple):
    print("Block Tuple(", multiprocessing.current_process().name, "):", block_tuple)
    earliest_block = block_tuple[0]
    # earliest_block = 4643576
    current_block = earliest_block
    latest_block = block_tuple[1]
    # latest_block = 4643579

    block_timestamps_map = dict()

    req = requests.Session()

    with open('json_requests/get_block_details.json') as json_data:
        data = json.load(json_data)

    # for block_number in range(earliest_block, latest_block+1):
    while current_block != latest_block:
        # req = urllib.request.Request(config.CONFIGURATION['DEFAULT']['GETH_URL'])
        # req.add_header('Content-Type', 'application/json; charset=utf-8')

        data["params"][0] = hex(current_block)

        response_str = "**Default**"

        try:
            send_request(req, current_block, data, block_timestamps_map)
            current_block += 1
            # print("Good Block:", current_block)
            if current_block % 100000 == 0:
                print("Progress (", multiprocessing.current_process().name, "):", round((current_block - earliest_block) / (latest_block - earliest_block) * 100, 4))
        except ValueError as e:
            print("Erroneous Block:", current_block, "******** Exception: ", e)
            block_timestamps_map[current_block] = response_str
            current_block += 1
        except ConnectionError:
            pass
        except:
            sys.stdout.write("\n")
            raise

    # print(block_timestamps_map)

    return block_timestamps_map


def send_request(req, current_block, data, block_timestamps_map):
    # with contextlib.closing(urllib.request.urlopen(req, json.dumps(data).encode("utf-8")).read()) as response:
    # response = urllib.request.urlopen(req, json.dumps(data).encode("utf-8")).read()
    # response = requests.post(config.CONFIGURATION['DEFAULT']['GETH_URL'], json=data, headers={'Content-Type': 'application/json; charset=utf-8'})
    response = req.post(config.CONFIGURATION['DEFAULT']['GETH_URL'], json=data)
    # block_details = json.loads(response.strip())["result"]
    # print("%r" % response.json())
    block_details = response.json()["result"]

    sys.stdout.write("\rBlock: %s" % current_block)

    # if current_block == 4643576:
    #     print("Response:", response)
    #     print(block_details.keys())
    #     print(block_details['logsBloom'])

    block_data = dict()
    block_data['difficulty'] = block_details["difficulty"].strip()
    block_data['extraData'] = block_details["extraData"].strip()
    block_data['gasLimit'] = block_details["gasLimit"].strip()
    block_data['gasUsed'] = block_details["gasUsed"].strip()
    block_data['hash'] = block_details["hash"].strip()
    block_data['miner'] = block_details["miner"].strip()
    block_data['mixHash'] = block_details["mixHash"].strip()
    block_data['nonce'] = block_details["nonce"].strip()
    block_data['number'] = block_details["number"].strip()
    block_data['parentHash'] = block_details["parentHash"].strip()
    block_data['receiptsRoot'] = block_details["receiptsRoot"].strip()
    block_data['size'] = block_details["size"].strip()
    block_data['stateRoot'] = block_details["stateRoot"].strip()
    block_data['timestamp'] = block_details["timestamp"].strip()
    block_data['totalDifficulty'] = block_details["totalDifficulty"].strip()
    block_data['transactionsRoot'] = block_details["transactionsRoot"].strip()
    # print(datetime.fromtimestamp(int(block_details["timestamp"].strip(), 16)))

    block_timestamps_map[current_block] = block_data

    # response_str = str(response)
    # print(response_str)
    # timestamp = int(response_str[response_str.find('"timestamp"') + 13:][0:response_str[response_str.find('"timestamp"') + 13:].find('"')], 16)
    # block_timestamps_map[current_block] = datetime.fromtimestamp(timestamp)
    # block_timestamps_map[current_block] = response_str
