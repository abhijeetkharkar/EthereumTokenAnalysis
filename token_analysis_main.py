from extractors import extract_bat_transfer_logs as ebtl
from extractors import extract_block_timestamps as ebt
from extractors import extract_bat_create_logs as ebcl
from utilities import config
from multiprocessing import Pool
import pickle
from dao import load_data


if __name__ == "__main__":
    config.init()
    mode = "load"
    instruction = "bat_transfer_events"

    if mode == "extraction":
        if instruction == "bat_transfer_events":
            ebtl.get_bat_transfer_logs()
        elif instruction == "bat_create_events":
            ebcl.get_bat_create_logs()
        elif instruction == "block_details":
            batches = [(3788557, 4073562), (4073562, 4358568), (4358568, 4643574), (4643574, 4928579), (4928579, 5213585),
                       (5213585, 5300000), (5300000, 5400000), (5400000, 5498591), (5498591, 5783596), (5783596, 6068602), (6068602, 6353608), (6353608, 6638615)]
            # earliest_block = 3788557
            current_batch = 5
            earliest_block = batches[current_batch][0]
            latest_block = batches[current_batch][1]
            # latest_block = 6638613
            process_count = 1

            # input_list = list()
            # size = latest_block - earliest_block + 1
            # for i in range(process_count):
            #     if i < process_count - 1:
            #         input_list.append((int(i * size / process_count) + earliest_block, int((i + 1) * size / process_count) + earliest_block))
            #     else:
            #         input_list.append((int(i * size / process_count) + earliest_block, int((i + 1) * size / process_count) + earliest_block + 1))
            # print(input_list)
            # p = Pool(processes=process_count)
            # chunks = p.map(ebt.get_block_details, input_list)
            # p.close()

            chunks = [ebt.get_block_details(batches[current_batch])]

            block_timestamps_dump = open("pickled_objects/block_timestamps_map_" + str(current_batch), "wb")
            pickle.dump(chunks, block_timestamps_dump)
    elif mode == "load":
        if instruction == "bat_transfer_events":
            load_data.load_bat_transfers()
        elif instruction == "bat_create_events":
            load_data.load_bat_create_events()
