from utilities import db_operations
from utilities import misc_operations
import networkx as nx
from datetime import datetime
from time import time
from datetime import date
from datetime import timedelta
import matplotlib.dates
import operator


def generate_graph_nx(limit="ALL"):
    print("Graph generation started", str(datetime.today()))
    query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE LOG"
    if limit == "ALL":
        records = db_operations.select_records(True, {"query": query})
    else:
        records = db_operations.select_records(True, {"query": query + " LIMIT " + str(limit)})
    bat_transfer_graph = nx.Graph()
    for record in records:
        bat_transfer_graph.add_edge(record[0], record[1], weight=(record[2], record[3]))
    # print(bat_transfer_graph.number_of_nodes())
    # print(list(nx.bfs_edges(bat_transfer_graph, "0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204")))
    directed_bat_transfer_graph = nx.DiGraph(bat_transfer_graph)
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
    return bfs_tree_levels[level]


def generate_component_evolution_graphs_per_month(seed_date="2017-05-29"):
    print("Component Analysis started", str(datetime.today()))
    current_date = datetime.strptime(seed_date, "%Y-%m-%d")
    end_date = datetime.strptime("2018-10-11", "%Y-%m-%d")
    # end_date = datetime.strptime("2017-07-28", "%Y-%m-%d")
    x_data = []
    number_of_scc = []
    component_size_range = {"Size 1": [], "Size 2 - 10": [], "Size 11 - 100": [], "Size 101 - 1000": [],
                            "Size 1001 - 10000": [], "Size >10000": []}
    largest_sccs = []
    while current_date < end_date:
        # query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE TIMESTAMP BETWEEN " \
        #         + str(current_date.timestamp()) + " AND " + str((current_date + timedelta(weeks=4)).timestamp())
        query = "SELECT FROM_ADDRESS, TO_ADDRESS, TIMESTAMP, DATA_FLOAT FROM TRANSFER_EVENTS WHERE TIMESTAMP < " + str((current_date + timedelta(weeks=4)).timestamp())
        records = db_operations.select_records(True, {"query": query})
        # print(query)
        bat_transfer_graph = nx.Graph()
        for record in records:
            bat_transfer_graph.add_edge(record[0], record[1], weight=(record[2], record[3]))
        directed_bat_transfer_graph = nx.DiGraph(bat_transfer_graph)
        scc = [component for component in nx.strongly_connected_component_subgraphs(directed_bat_transfer_graph)]
        x_data.append(datetime.strftime(current_date + timedelta(weeks=4), "%Y-%m-%d"))
        number_of_scc.append(len(scc))

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

        sub_graphs = [sg for sg in scc]
        top_5_scc_size = [len(sub_graph.nodes) for sub_graph in sub_graphs]
        top_5_scc_size.sort(reverse=True)
        degree_distribution_each_sub_graph_sorted_by_degree = [sorted(sg.degree, key=lambda x: x[1], reverse=True) for sg in sub_graphs]
        degree_distribution_each_sub_graph_sorted_by_degree.sort(key=lambda x: -len(x))
        # highest_degree_node_in_each_scc = [degree_distribution[0][0] for degree_distribution in
        # [sorted(sg.degree, key=lambda x: x[1], reverse=True) for sg in components_sg]]
        top_5_largest_components_with_highest_degree_node_in_them = [component[0] for component in degree_distribution_each_sub_graph_sorted_by_degree[0:5]]

        largest_sccs.append(top_5_scc_size[0])

        print("Highest Degree Nodes in Top 5 Largest SCC till", datetime.strftime((current_date + timedelta(weeks=4)), "%Y-%m-%d"), ":\n", top_5_scc_size[0:5], "\n", top_5_largest_components_with_highest_degree_node_in_them)

        component_size_range.get("Size 1").append(bin_1)
        component_size_range.get("Size 2 - 10").append(bin_2)
        component_size_range.get("Size 11 - 100").append(bin_3)
        component_size_range.get("Size 101 - 1000").append(bin_4)
        component_size_range.get("Size 1001 - 10000").append(bin_5)
        component_size_range.get("Size >10000").append(bin_6)

        current_date = current_date + timedelta(weeks=4)

    # print(component_size_range)

    for bin_name in component_size_range:
        component_size_range[bin_name] = (x_data, component_size_range.get(bin_name))

    misc_operations.plot_basic_bar_chart(x_data, number_of_scc, "#Strongly_Connected_Components v/s Date", "Date", "#SCC")

    misc_operations.plot_basic_bar_chart(x_data, largest_sccs, "Largest_Strongly_Connected_Components v/s Date", "Date", "Size")

    misc_operations.plot_multiple_lines_chart(component_size_range, "Frequency_of_Bins_of_Strongly_Connected_Components v/s Date",
                                              "Date", "Frequency", date=False)

    print("Component Analysis ended", str(datetime.today()))


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
    x_data = []
    y_data = []
    for i in range(20):
        x_data.append(in_degree_map_descending[i][0][26:36])
        y_data.append(in_degree_map_descending[i][1])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top In-Degree Nodes (keeping Multi-edges)", "Address", "Degree", 6)

    x_data = []
    y_data = []
    for i in range(20):
        x_data.append(out_degree_map_descending[i][0][26:36])
        y_data.append(out_degree_map_descending[i][1])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top Out-Degree Nodes (keeping Multi-edges)", "Address", "Degree", 6)

    x_data = []
    y_data = []
    for i in range(20):
        x_data.append(in_degree_multi_edge_merged_count_map_descending[i][0][26:36])
        y_data.append(in_degree_multi_edge_merged_count_map_descending[i][1])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top In-Degree Nodes (merging Multi-edges)", "Address", "Degree", 6)

    x_data = []
    y_data = []
    for i in range(20):
        x_data.append(out_degree_multi_edge_merged_count_map_descending[i][0][26:36])
        y_data.append(out_degree_multi_edge_merged_count_map_descending[i][1])
    misc_operations.plot_basic_bar_chart(x_data, y_data, "Top Out-Degree Nodes (merging Multi-edges)", "Address", "Degree", 6)

    print("In-Degree Out-Degree Analysis ended", str(datetime.today()))


def generate_betweenness_centrality_plots():
    print("Betweenness Centrality Analysis started", str(datetime.today()))
    graph = misc_operations.dump_load_pickle_object("load", "pickled_objects/transfer_events_graph_nx")
    betweenness_centrality = nx.betweenness_centrality(graph)
    misc_operations.dump_load_pickle_object("dump", "pickled_objects/betweenness_centrality_map", betweenness_centrality)
    print("Betweenness Centrality Analysis ended", str(datetime.today()))


def is_there_a_path(source, destination):
    graph = misc_operations.dump_load_pickle_object("load", "pickled_objects/transfer_events_graph_nx")
    print(nx.has_path(graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target="0x0000000000000000000000007a5e4424bf67acc5ec6751f79aebd7ec9b896cd3"))
    print(nx.shortest_path_length(graph, source="0x00000000000000000000000088e2efac3d2ef957fcd82ec201a506871ad06204", target="0x0000000000000000000000007a5e4424bf67acc5ec6751f79aebd7ec9b896cd3"))
