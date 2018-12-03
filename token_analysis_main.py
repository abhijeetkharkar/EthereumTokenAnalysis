from extractors import extract_bat_transfer_logs as ebtl
from extractors import extract_block_timestamps as ebt
from extractors import extract_bat_create_logs as ebcl
from utilities import config
from utilities import misc_operations
from multiprocessing import Pool
import pickle
from dao import load_data
from analyzers import analyze_bat_transfer_logs as abtl


if __name__ == "__main__":
    config.init()
    mode = "analyze"
    instruction = "average_distance_computation"

    if mode == "extraction":
        if instruction == "bat_transfer_events":
            ebtl.get_bat_transfer_logs()
        elif instruction == "bat_create_events":
            ebcl.get_bat_create_logs()
        elif instruction == "block_details":
            batches = [(3788557, 4073562), (4073562, 4358568), (4358568, 4643574), (4643574, 4928579),
                       (4928579, 5213585), (5213585, 5300000), (5300000, 5400000), (5400000, 5498591),
                       (5498591, 5783596), (5783596, 6068602), (6068602, 6353608), (6353608, 6638615)]
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
    elif mode == "analyze":
        if instruction == "graph_generation":  # One time generation as a pickle object is created and stored for future use
            abtl.generate_graph_nx()
        elif instruction == "bfs_tree":
            abtl.get_bfs_tree_level_nodes(3, '0x000000000000000000000000ce8d78428f969e3f2437e274f5068c0e2344be36')
        elif instruction == "strongly_connected_components_evolution_analysis":
            abtl.generate_component_evolution_graphs_per_month()
        elif instruction == "transaction_analysis":
            abtl.generate_transaction_plots()
        elif instruction == "degree_analysis":
            abtl.generate_indegree_outdegree_plots()
        elif instruction == "betweenness_centrality_analysis":
            abtl.generate_betweenness_centrality_plots()
        elif instruction == "check_path":
            abtl.is_there_a_path(source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204",
                                 destination="0x000000000000000000000000fb0ee19f427a09d28efe23b73c3e95c8789df9b7")
        elif instruction == "average_distance_computation":
            abtl.generate_average_distance_of_scc_from_brave()
        elif instruction == "create_gephi_graph":
            abtl.create_gephi_graph()
