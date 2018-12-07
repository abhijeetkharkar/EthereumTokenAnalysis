from utilities import db_operations
from utilities import misc_operations
import networkx as nx
from datetime import datetime
from datetime import timedelta
import matplotlib.dates
import operator
import numpy as np
import os
import sys
from multiprocessing import Pool
import multiprocessing


def generate_graph_nx(limit="ALL"):
    print("Graph generation started", str(datetime.today()))
    query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})
    directed_bat_transfer_graph = nx.DiGraph()
    for record in records:
        directed_bat_transfer_graph.add_edge(record[0], record[1], weight=(record[2], record[3]))
    misc_operations.dump_load_pickle_object("dump", "pickled_objects/transfer_events_graph_nx", directed_bat_transfer_graph)
    print("Graph generation ended", str(datetime.today()))


def generate_graph(limit="ALL"):
    print("Graph generation started", str(datetime.today()))
    query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})
    bat_transfer_graph = dict()
    for record in records:
        if record[0] in bat_transfer_graph:
            is_present = False
            index = -1
            count = 0
            for adjacent in bat_transfer_graph.get(record[0]):
                if record[1] == adjacent[0]:
                    is_present = True
                    index = count
                    break
                count += 1
            if not is_present:
                bat_transfer_graph.get(record[0]).append((record[1], ([record[2]], [record[3]])))
            else:
                bat_transfer_graph.get(record[0])[index][1][0].append(record[2])
                bat_transfer_graph.get(record[0])[index][1][1].append(record[3])
        else:
            bat_transfer_graph[record[0]] = [(record[1], ([record[2]], [record[3]]))]
    # print(bat_transfer_graph.get("0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204"))
    print("Graph generation ended", str(datetime.today()))
    misc_operations.dump_load_pickle_object("dump", "pickled_objects/transfer_events_graph", bat_transfer_graph)


def get_bfs_tree_level_nodes(level=0, root="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204"):
    print("BFS Tree level nodes generation started", str(datetime.today()))
    graph = misc_operations.dump_load_pickle_object("load", "pickled_objects/transfer_events_graph")
    # for from_address in graph:
    #         for tuples in graph.get(from_address):
    #                 if len(tuples[1][0]) > 1:
    #                     print(graph[from_address])
    #                     break
    if type(root) == str:
        if root not in graph:
            raise ValueError("Invalid Root")
        # bfs_tree_levels = bfs(graph, root)

        # unvisited_nodes => list(address)
        unvisited_nodes = list(graph.keys())
        unvisited_nodes.remove(root)

        # print(unvisited_nodes.count("0x00000000000000000000000067fa2c06c9c6d4332f330e14a66bdf1873ef3d2b"))

        # current_level => list(tuple(tuple(address, tuple(timestamp, #bat)), parent_address))
        current_level = [((root, (None, None)), None)]

        # bfs_tree_levels => list(list(tuple(tuple(address, tuple(timestamp, #bat)), parent_address)))
        bfs_tree_levels = [[((root, (None, None)), None)]]
    else:
        unvisited_nodes = list(graph.keys())
        current_level = []
        for node in root:
            current_level.append(((node, (None, None)), None))
            if node in unvisited_nodes:
                unvisited_nodes.remove(node)
        bfs_tree_levels = [current_level]

    while len(unvisited_nodes) != 0:
        # print(current_level)
        temp_level = []
        for parent in current_level:
            children = graph.get(parent[0][0])
            if children is not None:
                for child in children:
                    if unvisited_nodes.count(child[0]) != 0:
                        temp_level.append((child, parent[0][0]))
                        unvisited_nodes.remove(child[0])
        if len(temp_level) == 0:
            break
        else:
            bfs_tree_levels.append(temp_level)
            current_level = temp_level

    for index in range(len(bfs_tree_levels)):
        print("Level", index, ":", len(bfs_tree_levels[index]))
    print("BFS Tree level nodes generation ended", str(datetime.today()))
    if level == "ALL":
        return bfs_tree_levels
    else:
        return bfs_tree_levels[level]


def generate_component_evolution_graphs_per_month(seed_date="2017-05-29"):
    print("Component Analysis started", str(datetime.today()))
    current_date = datetime.strptime(seed_date, "%Y-%m-%d")
    end_date = datetime.strptime("2018-11-09", "%Y-%m-%d")
    # end_date = datetime.strptime("2017-07-28", "%Y-%m-%d")
    x_data = []
    number_of_scc = []
    component_size_range = {"Size 1": [], "Size 2 - 10": [], "Size 11 - 100": [], "Size 101 - 1000": [],
                            "Size 1001 - 10000": [], "Size >10000": []}
    largest_sccs = []
    node_list_as_time_progresses = []
    max_size_node_list = 0
    while True:
        # query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE TIMESTAMP BETWEEN " \
        #         + str(current_date.timestamp()) + " AND " + str((current_date + timedelta(weeks=4)).timestamp())
        query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE TIMESTAMP < " + str((current_date + timedelta(weeks=4)).timestamp())
        records = db_operations.select_records(True, {"query": query})

        directed_bat_transfer_graph = nx.DiGraph()
        for record in records:
            directed_bat_transfer_graph.add_edge(record[0], record[1], weight=(record[2], record[3]))
        # directed_bat_transfer_graph = nx.DiGraph(bat_transfer_graph)
        scc = [component for component in nx.strongly_connected_component_subgraphs(directed_bat_transfer_graph)]

        # directed_bat_transfer_graph = nx.DiGraph()
        # directed_bat_transfer_graph.add_edge('b', 'a')
        # directed_bat_transfer_graph.add_edge('a', 'c')
        # directed_bat_transfer_graph.add_edge('c', 'd')
        # directed_bat_transfer_graph.add_edge('d', 'b')
        # directed_bat_transfer_graph.add_edge('c', 'b')
        # directed_bat_transfer_graph.add_node('e')
        # directed_bat_transfer_graph.add_node('f')
        # scc = [component for component in nx.strongly_connected_component_subgraphs(directed_bat_transfer_graph)]

        x_data.append(datetime.strftime(current_date + timedelta(weeks=4), "%Y-%m-%d"))
        number_of_scc.append(len(scc))

        # Binning
        bin_1 = 0
        bin_2 = 0
        bin_3 = 0
        bin_4 = 0
        bin_5 = 0
        bin_6 = 0
        max_size = 0
        for component in scc:
            if 0 < len(component.nodes) <= 1:
                bin_1 += 1
            elif 1 < len(component.nodes) <= 10:
                bin_2 += 1
            elif 10 < len(component.nodes) <= 100:
                bin_3 += 1
            elif 100 < len(component.nodes) <= 1000:
                bin_4 += 1
            elif 1000 < len(component.nodes) <= 10000:
                bin_5 += 1
            else:
                bin_6 += 1

            if len(component.nodes) > max_size:
                max_size = len(component.nodes)

        component_size_range.get("Size 1").append(bin_1)
        component_size_range.get("Size 2 - 10").append(bin_2)
        component_size_range.get("Size 11 - 100").append(bin_3)
        component_size_range.get("Size 101 - 1000").append(bin_4)
        component_size_range.get("Size 1001 - 10000").append(bin_5)
        component_size_range.get("Size >10000").append(bin_6)

        sub_graphs = [sg for sg in scc]

        # Size of the Largest SCC
        top_5_scc_size = [len(sub_graph.nodes) for sub_graph in sub_graphs]
        top_5_scc_size.sort(reverse=True)
        largest_sccs.append(top_5_scc_size[0])

        # Top-5 Largest SCCs with Top-5 highest degree nodes in them (degree = in_degree + out_degree + in_degree * out_degree)
        degree_distribution_each_sub_graph_sorted_by_degree = list()
        for sg in sub_graphs:
            in_degree_list = list(sg.in_degree)
            out_degree_list = list(sg.out_degree)
            in_degree_list = sorted(in_degree_list, key=lambda x: x[0])
            out_degree_list = sorted(out_degree_list, key=lambda x: x[0])
            # for i in range(len(in_degree_list)):
            #     if in_degree_list[i][1] != out_degree_list[i][1]:
            #         raise ValueError("Good")
            sg_degree_recomputed = list()

            for index in range(len(in_degree_list)):
                node = in_degree_list[index][0]
                in_degree = in_degree_list[index][1]
                out_degree = out_degree_list[index][1]
                sg_degree_recomputed.append((node, in_degree + out_degree + in_degree * out_degree, in_degree, out_degree))

            sg_degree_recomputed = sorted(sg_degree_recomputed, key=lambda x: x[1], reverse=True)
            # print(len(sg.nodes), ":::::", sg_degree_recomputed)
            degree_distribution_each_sub_graph_sorted_by_degree.append(sg_degree_recomputed)

        degree_distribution_each_sub_graph_sorted_by_degree.sort(key=lambda x: -len(x))

        top_5_largest_components_with_top_5_highest_degree_nodes_in_them = [component[0:5] for component in degree_distribution_each_sub_graph_sorted_by_degree[0:5]]

        print("Highest Degree Nodes in Top 5 Largest SCC till", datetime.strftime((current_date + timedelta(weeks=4)), "%Y-%m-%d"), ":\n", top_5_scc_size[0:5], "\n", top_5_largest_components_with_top_5_highest_degree_nodes_in_them)

        # Intersection of Sets of Nodes involved in top few SCC excluding the astronomical SCC
        sub_graphs_sorted = sorted(sub_graphs, key=lambda x: len(x.nodes), reverse=True)[1:]
        node_limit = 200
        total_nodes = 0
        node_list = []
        for sg in sub_graphs_sorted:
            nodes = list(sg.nodes)
            total_nodes += len(nodes)
            node_list.extend(nodes)
            if total_nodes > node_limit:
                break
        node_list_as_time_progresses.append(set(node_list))
        if max_size_node_list < len(node_list):
            max_size_node_list = len(node_list)

        percent_similarity = len(set.intersection(*node_list_as_time_progresses)) / max_size_node_list * 100
        print("Percent Similarity In Smaller Components:", percent_similarity)
        print("Intersecting Addresses:", set.intersection(*node_list_as_time_progresses))

        # Calling the Average and Median Distance from Brave Calculator
        # generate_average_distance_of_scc_from_brave(directed_bat_transfer_graph, scc, datetime.strftime(current_date + timedelta(weeks=4), "%Y-%m-%d"))

        if current_date + timedelta(weeks=4) > end_date:
            break
        else:
            current_date += timedelta(weeks=4)

    # print(component_size_range)

    for bin_name in component_size_range:
        component_size_range[bin_name] = (x_data, component_size_range.get(bin_name))

    misc_operations.plot_basic_bar_chart(x_data, number_of_scc, "#Strongly_Connected_Components v/s Date", "Date", "#SCC", x_label_font_size=7)

    misc_operations.plot_basic_bar_chart(x_data, largest_sccs, "Largest_Strongly_Connected_Components v/s Date", "Date", "Size", x_label_font_size=7)

    misc_operations.plot_multiple_lines_chart(component_size_range, "Frequency_of_Bins_of_Strongly_Connected_Components v/s Date",
                                              "Date", "Frequency", date=False, x_label_font_size=7)

    component_size_range.pop("Size 1", None)

    misc_operations.plot_multiple_lines_chart(component_size_range,
                                              "Frequency_of_Bins_of_Strongly_Connected_Components (w.o. most frequent bin) v/s Date",
                                              "Date", "Frequency", date=False, x_label_font_size=7)

    node_list_as_time_progresses.sort(key=lambda x: len(x), reverse=True)
    percent_similarity = len(set.intersection(*node_list_as_time_progresses)) / len(node_list_as_time_progresses[0]) * 100
    print("Node List:", node_list_as_time_progresses)
    # print("Max(sorted):", len(node_list_as_time_progresses[0]), "|", "Max(variable):", max_size_node_list)
    print("Percent Similarity In Smaller Components:", percent_similarity)

    print("Component Analysis ended", str(datetime.today()))


def generate_average_distance_of_scc_from_brave(seed_date="2017-05-29"):
    print("Avg. Distance Computation started", str(datetime.today()))

    current_date = datetime.strptime(seed_date, "%Y-%m-%d")
    end_date = datetime.strptime("2018-11-09", "%Y-%m-%d")
    # end_date = datetime.strptime("2017-08-09", "%Y-%m-%d")

    x_data = []
    number_of_scc = []

    while True:

        query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE TIMESTAMP < " + str((current_date + timedelta(weeks=4)).timestamp())
        records = db_operations.select_records(True, {"query": query})

        directed_bat_transfer_graph = nx.DiGraph()
        for record in records:
            directed_bat_transfer_graph.add_edge(record[0], record[1], weight=(record[2], record[3]))

        sccs = [component for component in nx.strongly_connected_component_subgraphs(directed_bat_transfer_graph)]
        sccs.sort(key=lambda x: len(x.nodes), reverse=True)

        x_data.append(datetime.strftime(current_date + timedelta(weeks=4), "%Y-%m-%d"))

        sys.stdout.write("\rCurrent Execution Date: " + datetime.strftime(current_date + timedelta(weeks=4), "%Y-%m-%d"))
        print()

        data_map = {"mean": [[], []], "median": [[], []]}
        index = 1
        number_ssc_less_than_6_hops_away = 0
        for scc in sccs[1:]:
            sys.stdout.write("\rPercent Completion: " + str(round(float(index-1)/float(len(sccs)) * 100, 3)))
            nodes = list(scc.nodes)
            distance_list = []
            if "0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204" in nodes:
                data_map.get("mean")[0].append("00")
                data_map.get("median")[0].append("00")
            else:
                data_map.get("mean")[0].append(str(index))
                data_map.get("median")[0].append(str(index))

            for node in nodes:
                if nx.has_path(directed_bat_transfer_graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target=node):
                    distance_list.append(nx.shortest_path_length(directed_bat_transfer_graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target=node))
                else:
                    distance_list.append(10000)

            for node in nodes:
                if nx.has_path(directed_bat_transfer_graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target=node) and nx.shortest_path_length(directed_bat_transfer_graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target=node) < 6:
                    number_ssc_less_than_6_hops_away += 1
                    break

            data_map.get("mean")[1].append(np.mean(distance_list))
            data_map.get("median")[1].append(np.median(distance_list))
            index += 1

        number_of_scc.append(number_ssc_less_than_6_hops_away)

        # print(data_map)

        if current_date + timedelta(weeks=4) > end_date:
            break
        else:
            current_date += timedelta(weeks=4)

    # misc_operations.plot_multiple_lines_chart(data_map, "Average distance of SCCs from Brave till " + date, "SCC", "Hops", x_label_font_size=4)
    misc_operations.plot_basic_bar_chart(x_data, number_of_scc, "#SCC greater than 6 Hops Away from Brave as Time progresses", "Date", "#SCC", x_label_font_size=7)
    print("Avg. Distance Computation ended", str(datetime.today()))


def generate_transaction_plots(limit="ALL"):
    print("Plot generation started", str(datetime.today()))
    query = "SELECT DATE(TIMESTAMP, 'unixepoch', 'localtime'), COUNT(1), SUM(DATA_FLOAT), AVG(DATA_FLOAT) FROM TRANSFER_EVENTS WHERE TIMESTAMP != 0 GROUP BY DATE(TIMESTAMP, 'unixepoch', 'localtime') ORDER BY TIMESTAMP"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})

    x_data = []
    y_data_number_transactions = []
    y_data_number_transactions_downscaled = []
    y_data_sum = []
    y_data_sum_downscaled = []
    y_data_avg = []
    y_data_avg_downscaled = []
    for record in records:
        if datetime.strptime(record[0], '%Y-%m-%d').date() > datetime.strptime('2017-06-01', '%Y-%m-%d').date():
            x_data.append(datetime.strptime(record[0], '%Y-%m-%d').date())
            y_data_number_transactions.append(record[1])
            y_data_number_transactions_downscaled.append(float(record[1])/1000.0)
            y_data_sum.append(int(record[2]))
            y_data_sum_downscaled.append(float(int(record[2])) / 100000000.0)
            y_data_avg.append(int(record[3]))
            y_data_avg_downscaled.append(float(int(record[3])) / 10000000.0)

    data_map = dict()
    # data_map["#Transactions (X $10^3$)"] = (x_data, y_data_number_transactions_downscaled)
    data_map["Total BAT Transferred (X $10^8$)"] = (matplotlib.dates.date2num(x_data), y_data_sum_downscaled)
    data_map["Avg. BAT Transferred (X $10^7$)"] = (matplotlib.dates.date2num(x_data), y_data_avg_downscaled)

    misc_operations.plot_basic_line_chart(x_data, y_data_number_transactions, "#Transactions v/s Date", "Date",
                                          "#Transactions", date=True)
    misc_operations.plot_basic_line_chart(x_data, y_data_sum, "Total BAT Transferred v/s Date", "Date",
                                          "Total BAT Transferred", date=True)
    misc_operations.plot_basic_line_chart(x_data, y_data_avg, "Avg BAT Transferred v/s Date", "Date",
                                          "Avg. BAT Transferred", date=True)

    misc_operations.plot_multiple_lines_chart(data_map, "BAT Transferred v/s Date", "Date", "BAT Transferred", date=True)

    print("Plot generation ended", str(datetime.today()))


def generate_indegree_outdegree_plots(limit="ALL"):
    print("In-Degree Out-Degree Analysis started", str(datetime.today()))
    query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})

    in_degree_multi_edge_merged_map = dict()
    out_degree_multi_edge_merged_map = dict()
    in_degree_map = dict()
    out_degree_map = dict()
    for record in records:
        if record[0] in out_degree_map:
            out_degree_map[record[0]] += 1
        else:
            out_degree_map[record[0]] = 1

        if record[1] in in_degree_map:
            in_degree_map[record[1]] += 1
        else:
            in_degree_map[record[1]] = 1

        if record[0] in out_degree_multi_edge_merged_map:
            out_degree_multi_edge_merged_map[record[0]].add(record[1])
        else:
            out_degree_multi_edge_merged_map[record[0]] = {record[1]}

        if record[1] in in_degree_multi_edge_merged_map:
            in_degree_multi_edge_merged_map[record[1]].add(record[0])
        else:
            in_degree_multi_edge_merged_map[record[1]] = {record[0]}

    in_degree_multi_edge_merged_count_map = dict()
    out_degree_multi_edge_merged_count_map = dict()

    for address in in_degree_multi_edge_merged_map:
        in_degree_multi_edge_merged_count_map[address] = len(in_degree_multi_edge_merged_map.get(address))

    for address in out_degree_multi_edge_merged_map:
        out_degree_multi_edge_merged_count_map[address] = len(out_degree_multi_edge_merged_map.get(address))

    in_degree_map_descending = sorted(in_degree_map.items(), key=operator.itemgetter(1), reverse=True)
    out_degree_map_descending = sorted(out_degree_map.items(), key=operator.itemgetter(1), reverse=True)

    in_degree_multi_edge_merged_count_map_descending = sorted(in_degree_multi_edge_merged_count_map.items(), key=operator.itemgetter(1), reverse=True)
    out_degree_multi_edge_merged_count_map_descending = sorted(out_degree_multi_edge_merged_count_map.items(), key=operator.itemgetter(1), reverse=True)

    # print(in_degree_map_descending)
    # print(out_degree_multi_edge_merged_count_map_descending)

    x_set = set()

    x_data = []
    y_data = []
    for i in range(10):
        x_data.append(in_degree_map_descending[i][0][26:30])
        y_data.append(in_degree_map_descending[i][1])
        x_set.add(in_degree_map_descending[i][0])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top In-Degree Nodes (keeping Multi-edges)", "Address", "Degree", 12)

    x_data = []
    y_data = []
    for i in range(10):
        x_data.append(out_degree_map_descending[i][0][26:30])
        y_data.append(out_degree_map_descending[i][1])
        x_set.add(out_degree_map_descending[i][0])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top Out-Degree Nodes (keeping Multi-edges)", "Address", "Degree", 12)

    x_data = []
    y_data = []
    for i in range(10):
        x_data.append(in_degree_multi_edge_merged_count_map_descending[i][0][26:30])
        y_data.append(in_degree_multi_edge_merged_count_map_descending[i][1])
        x_set.add(in_degree_multi_edge_merged_count_map_descending[i][0])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top In-Degree Nodes (merging Multi-edges)", "Address", "Degree", 12)

    x_data = []
    y_data = []
    for i in range(10):
        x_data.append(out_degree_multi_edge_merged_count_map_descending[i][0][26:30])
        y_data.append(out_degree_multi_edge_merged_count_map_descending[i][1])
        x_set.add(out_degree_multi_edge_merged_count_map_descending[i][0])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top Out-Degree Nodes (merging Multi-edges)", "Address", "Degree", 12)

    print("Union of X-Data:")
    [print(address) for address in x_set]

    print("In-Degree Out-Degree Analysis ended", str(datetime.today()))


def generate_betweenness_centrality_plots():
    print("Betweenness Centrality Analysis started at", str(datetime.today()))
    process_count = 5
    input_list = [i for i in range(10)]
    p = Pool(processes=process_count)
    chunks = p.map(generate_betweenness_centrality_random_pivots, input_list)
    p.close()

    betweenness_centrality = dict()
    for chunk in chunks:
        for address in chunk:
            if address in betweenness_centrality:
                betweenness_centrality.get(address).append(chunk.get(address))
            else:
                betweenness_centrality[address] = [chunk.get(address)]

    misc_operations.dump_load_pickle_object("dump", "pickled_objects/betweenness_centrality_map", betweenness_centrality)

    betweenness_centrality_mean = {address: np.mean(betweenness_centrality.get(address)) for address in betweenness_centrality}

    betweenness_centrality = None

    sorted_betweenness_centrality_mean = sorted(betweenness_centrality_mean.items(), key=lambda x: x[1], reverse=True)

    for item in sorted_betweenness_centrality_mean[: 10]:
        print(item)

    print("Betweenness Centrality Analysis ended at", str(datetime.today()))


def generate_betweenness_centrality_random_pivots(dummy):
    print("Random Pivots started (", multiprocessing.current_process().name, ") at", str(datetime.today()))
    graph = misc_operations.dump_load_pickle_object("load", "pickled_objects/transfer_events_graph_nx")
    betweenness_centrality_random_pivot = nx.betweenness_centrality(graph, k=1000)
    print("Random Pivots ended (", multiprocessing.current_process().name, ") at", str(datetime.today()))
    return betweenness_centrality_random_pivot


def is_there_a_path(source, destination):
    graph = misc_operations.dump_load_pickle_object("load", "pickled_objects/transfer_events_graph_nx")
    print(len(graph.nodes))
    check = nx.has_path(graph, source=source, target=destination)
    print(check)
    if check:
        print(nx.shortest_path_length(graph, source=source, target=destination))


def create_gephi_graph():
    limit = "ALL"
    query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})

    directed_bat_transfer_graph_count = nx.DiGraph()
    directed_bat_transfer_graph_bat = nx.DiGraph()
    for record in records:
        directed_bat_transfer_graph_count.add_edge(record[0], record[1], weight=1)
        directed_bat_transfer_graph_bat.add_edge(record[0], record[1], weight=record[3])

    nx.write_gexf(directed_bat_transfer_graph_count, "output/gephi/transfer_events_graph_nx_count.gexf")
    nx.write_gexf(directed_bat_transfer_graph_bat, "output/gephi/transfer_events_graph_nx_bat.gexf")

