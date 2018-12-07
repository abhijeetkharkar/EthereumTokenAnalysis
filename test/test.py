import multiprocessing
import pickle
import networkx as nx
import operator as op


def f(x):
    print(multiprocessing.current_process().name)
    return x * x


def f1(i, map, v):
    map[i] = i
    v += 1


if __name__ == "__main__":
    # p = multiprocessing.Pool(processes=3)
    # print(p.map(f, range(200)))
    # for i in range(30):
    #     if i % 2 == 0:
    #         print("testing r", i, "\r")
    #     if i % 7 == 0:
    #         print(i)
    # map = dict()
    # v = 0
    # for i in range(10):
    #     f1(i, map, v)
    # print(map)
    # print(v)
    # with open('../pickled_objects/bat_transfer_events_list', "rb") as f:
    #     my_object = pickle.load(f)
    # print(len(my_object))

    graph = nx.DiGraph()
    graph.add_edge(1, 0)
    graph.add_edge(0, 2)
    graph.add_edge(2, 1)
    graph.add_edge(0, 3)
    graph.add_edge(3, 4)

    scc_sg = nx.strongly_connected_component_subgraphs(graph)
    components_sg = [sg for sg in scc_sg]
    sorted_degrees = [sorted(sg.degree, key=lambda x: x[1], reverse=True) for sg in components_sg]
    sorted_degrees.sort(key=lambda x: -len(x))
    print(sorted_degrees)
    # degree = [degree_distribution[0][0] for degree_distribution in sorted_degrees]

