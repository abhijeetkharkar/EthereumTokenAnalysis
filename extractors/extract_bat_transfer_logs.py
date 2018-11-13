import urllib.request
import json
from utilities import config
import pickle
from datetime import datetime


def get_bat_transfer_logs():
    print("Extraction of BAT Transfer Logs started", str(datetime.today()))

    earliest_block = 3788557
    events_list = []
    counter = 1
    index_after_last_pass = 0
    while True:
        req = urllib.request.Request(config.CONFIGURATION['DEFAULT']['GETH_URL'])
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        with open('json_requests/get_bat_transfer_logs.json') as json_data:
            data = json.load(json_data)

        data["params"][0]["fromBlock"] = hex(earliest_block)
        data["params"][0]["toBlock"] = hex(earliest_block + 50000)

        try:
            response = urllib.request.urlopen(req, json.dumps(data).encode("utf-8"))
            events_log = json.loads(response.read())["result"]

            print("Pass", counter, ", #Events:", len(events_log), "(Block -", earliest_block, "TO Block -", earliest_block+50000, ")")

            if len(events_log) == 0:
                break

            for events in events_log:
                event_data = {}
                for key in events.keys():
                    event_data[key.strip()] = events.get(key)
                events_list.append(event_data)

            earliest_block += 50001
            counter += 1
            index_after_last_pass = len(events_list)
        except ConnectionError:
            events_list = events_list[0:index_after_last_pass]

    print("Total Transactions:", len(events_list))
    # os.system("vmstat")
    # time.sleep(120)
    bat_transfer_events_dump = open("pickled_objects/bat_transfer_events_list", "wb")
    pickle.dump(events_list, bat_transfer_events_dump)

    print("Extraction of BAT Transfer Logs ended", str(datetime.today()))
