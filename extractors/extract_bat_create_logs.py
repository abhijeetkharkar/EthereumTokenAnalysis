import json
from utilities import config
import pickle
import requests
from datetime import datetime


def get_bat_create_logs():
    print("Extraction of BAT Create Logs started", str(datetime.today()))

    earliest_block = 3788557
    latest_block = 6738615

    req = requests.Session()

    with open('json_requests/get_bat_create_logs.json') as json_data:
        data = json.load(json_data)

    data["params"][0]["fromBlock"] = hex(earliest_block)
    data["params"][0]["toBlock"] = hex(latest_block)

    try:
        response = req.post(config.CONFIGURATION['DEFAULT']['GETH_URL'], json=data)
        events_list = response.json()["result"]
    except ConnectionError:
        raise
    except:
        raise

    print("Total Transactions:", len(events_list))

    bat_create_events_dump = open("pickled_objects/bat_create_events_list", "wb")
    pickle.dump(events_list, bat_create_events_dump)

    print("Extraction of BAT Create Logs ended", str(datetime.today()))
