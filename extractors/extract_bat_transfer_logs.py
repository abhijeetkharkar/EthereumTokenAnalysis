import urllib.request
import json
from config_files import config
import pickle


def get_bat_transfer_logs():
    earliest_block = 3788557
    # events_csv = open("output/bat_transfer_events.csv", "w")

    # print("To,From,Data,Block Number,Transaction Hash,Transaction Index,Block Hash,Log Index")
    # events_csv.write("To,From,Data,Block Number,Transaction Hash,Transaction Index,Block Hash,Log Index\n")
    events_list = []
    counter = 1
    index_after_last_pass = 0
    while True:
        req = urllib.request.Request(config.CONFIGURATION['DEFAULT']['GETH_URL'])
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        with open('json_requests/get_bat_transfer_logs.json') as json_data:
            data = json.load(json_data)

        # print(data)
        # print(data["params"][0]["fromBlock"])

        data["params"][0]["fromBlock"] = hex(earliest_block)
        data["params"][0]["toBlock"] = hex(earliest_block + 50000)

        # print(data)
        try:
            response = urllib.request.urlopen(req, json.dumps(data).encode("utf-8"))

            events_log = json.loads(response.read())["result"]

            print("Pass", counter, ", #Events:", len(events_log), "(Block -", earliest_block, "TO Block -", earliest_block+50000, ")")

            if len(events_log) == 0:
                break

            for events in events_log:
                row = ""
                event_data = {}
                for key in events.keys():
                    if key.strip() == "topics":
                        row += events.get(key)[1].strip() + ","
                        event_data[key.strip()] = events.get(key)[1].strip()
                    elif key.strip() == "removed":
                        pass
                    else:
                        # print(key.strip())
                        if key.strip() == "data":
                            row += str(int(events.get(key), 16) / 10**18) + ","
                            event_data[key.strip()] = int(events.get(key), 16) / 10**18
                        else:
                            row += events.get(key).strip() + ","
                            event_data[key.strip()] = events.get(key)[1].strip()
                # row = row[:-1]
                # print(row)
                events_list.append(event_data)
                # events_csv.write(row+"\n")
            earliest_block += 50001
            counter += 1
            index_after_last_pass = len(events_list)
        except ConnectionError:
            events_list = events_list[0:index_after_last_pass]
    bat_transfer_events_dump = open("pickled_objects/bat_transfer_events_list", "wb")
    pickle.dump(events_list, bat_transfer_events_dump)
    print("Total Transactions:", len(events_list))
