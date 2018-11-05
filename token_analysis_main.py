from extractors import extract_bat_transfer_logs as ebtl
from extractors import extract_block_timestamps as ebt
from config_files import config
from multiprocessing import Pool
import pickle


if __name__ == "__main__":
    config.init()
    mode = "extraction"
    instruction = "block_details"

    if mode == "extraction":
        if instruction == "bat_transfer_events":
            bat_transfer_data_main = ebtl.get_bat_transfer_logs()
        elif instruction == "block_details":
            earliest_block = 3788557
            latest_block = 6638613
            process_count = 1

            input_list = list()
            size = latest_block - earliest_block + 1
            for i in range(process_count):
                if i < process_count - 1:
                    input_list.append((int(i * size / process_count) + earliest_block, int((i + 1) * size / process_count) + earliest_block))
                else:
                    input_list.append((int(i * size / process_count) + earliest_block, int((i + 1) * size / process_count) + earliest_block + 1))

            p = Pool(processes=process_count)
            chunks = p.map(ebt.get_block_details, input_list)
            p.close()

            block_timestamps_dump = open("pickled_objects/block_timestamps_map", "wb")
            pickle.dump(chunks, block_timestamps_dump)

            # ebt.get_block_details((1, 2))
