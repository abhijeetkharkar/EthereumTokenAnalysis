import pickle
import sys
import os
from utilities import db_operations
from datetime import datetime
from decimal import Decimal


def load_block_details():
    # print(os.listdir('../pickled_objects'))
    block_details_map = dict()
    for filename in os.listdir('pickled_objects'):
        if filename.startswith("block_timestamps_map_"):
            current_file = open('pickled_objects/' + filename, 'rb')
            block_details_map = {**block_details_map, **pickle.load(current_file)[0]}
    # print(len(block_details_map))


def load_bat_transfers():
    print("Loading of BAT Transfer Events started at", str(datetime.today()))
    try:
        with open('pickled_objects/bat_transfer_events_list', "rb") as f:
            bat_transfers = pickle.load(f)
        # print(bat_transfers[100000])
        # print()
        data = []
        progress = ["|", "/", "--", "\\"]
        count = 0
        # TRANSACTION_HASH, TO_ADDRESS, FROM_ADDRESS, TIMESTAMP, DATA_HEX, DATA_INT, DATA_FLOAT, BLOCK_NUMBER, TRANSACTION_INDEX, BLOCK_HASH, LOG_INDEX
        for record in bat_transfers:
            if not record.get('removed'):
                row = [record.get('transactionHash'), record.get('topics')[2], record.get('topics')[1], 0,
                       record.get('data'), str(int(record.get('data'), 16)),
                       "{0:f}".format(Decimal(int(record.get('data'), 16)) / Decimal(10 ** 18)),
                       int(record.get('blockNumber'), 16), record.get('transactionIndex'), record.get('blockHash'),
                       record.get('logIndex')]
                data.append(tuple(row))
            else:
                print("\nInvalid Record:", record)
            sys.stdout.write("\rRow: " + str(count) + " " + progress[count % 4] + " Progress: " + str(round(count/len(bat_transfers)*100, 2)))
            count += 1

        # db_operations.insert_records_batch("TRANSFER_EVENTS", data, 10)
        db_operations.insert_records_batch("TRANSFER_EVENTS", data, 11, db_file="db/blockchain.db")
        print("\nLoading of BAT Transfer Events ended at", str(datetime.today()))
    except:
        raise


def load_bat_create_events():
    print("Loading of BAT Create Events started at", str(datetime.today()))
    try:
        with open('pickled_objects/bat_create_events_list', "rb") as f:
            bat_create_events = pickle.load(f)
        # print(bat_create_events[1])
        # print()
        data = []
        progress = ["|", "/", "--", "\\"]
        count = 0
        # TRANSACTION_HASH, TO_ADDRESS, FROM_ADDRESS, TIMESTAMP, DATA_HEX, DATA_INT, DATA_FLOAT, BLOCK_NUMBER, TRANSACTION_INDEX, BLOCK_HASH, LOG_INDEX
        for record in bat_create_events:
            if not record.get('removed'):
                row = [record.get('transactionHash'), record.get('topics')[1], record.get('address'), 0,
                       record.get('data'), str(int(record.get('data'), 16)),
                       "{0:f}".format(Decimal(int(record.get('data'), 16)) / Decimal(10 ** 18)),
                       int(record.get('blockNumber'), 16), record.get('transactionIndex'), record.get('blockHash'),
                       record.get('logIndex')]
                data.append(tuple(row))
            else:
                print("\nInvalid Record:", record)
            sys.stdout.write("\rRow: " + str(count) + " | Progress: " + str(round(count/len(bat_create_events)*100, 2)) + "..." + progress[count % 4])
            count += 1

        db_operations.insert_records_batch("CREATE_EVENTS", data, 11, db_file="db/blockchain.db")
        print("\nLoading of BAT Transfer Create ended at", str(datetime.today()))
    except:
        raise
