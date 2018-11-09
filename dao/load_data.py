import pickle
import sys
import os


def load_block_details():
    print(os.listdir('../pickled_objects'))
    block_details_map = dict()
    for filename in os.listdir('../pickled_objects'):
        if filename.startswith("block_timestamps_map_"):
            current_file = open('../pickled_objects/' + filename, 'rb')
            block_details_map = {**block_details_map, **pickle.load(current_file)[0]}
    print(len(block_details_map))


if __name__ == "__main__":
    load_block_details()
