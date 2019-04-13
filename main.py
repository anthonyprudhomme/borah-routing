import sys

import matplotlib.pyplot as plt
import networkx as nx
import prim
import kruskal
import math
import itertools
import time
import copy

current_milli_time = lambda: int(round(time.time() * 1000))

begining_timestamp = 0
after_mst_timestamp = 0
end_timestamp = 0

def check_for_input_errors():
    if(len(sys.argv) < 3):
        print('You must specify the file name you want to use and the method to accomplish MST')
        print('python main.py [filename].pts.txt [prim or kruskal]')
        return False
    if not sys.argv[1].endswith('.pts.txt'):
        print('You must specify a file name located in the Points folder of the project')
        print('e.g. python main.py filename.pts.txt [prim or kruskal]')
        return False
    if 'prim' != sys.argv[2].lower() and 'kruskal' != sys.argv[2].lower():
        print('You must specify the algorithm you want to choose (Prim or Kruskal)')
        print('e.g. python main.py filename.pts.txt prim')
        return False
    return True

def show_graph():
    node_position = nx.get_node_attributes(graph,'node_position')
    color_map = nx.get_node_attributes(graph,'node_color').values()
    nx.draw(graph, node_position, with_labels=True, node_color=color_map, font_weight='bold')
    plt.draw()
    plt.pause(1)
    plt.clf()

def find_best_node_edge_pairs(edges, nodes, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict):
    index_of_next_node = len(x_hanan_nodes) * len(y_hanan_nodes)
    gain_list = []
    for edge in edges:
        best_gain = 0
        best_node = None
        best_node_p = None
        node_p = None
        edge_to_remove = None
        for node in nodes:
            current_node = nodes[node]
            if not (edge.values()[0] is current_node or edge.values()[1] is current_node):
                x1 = edge.values()[0][0]
                y1 = edge.values()[0][1]
                x2 = edge.values()[1][0]
                y2 = edge.values()[1][1]
                x_first_hanan_index = x_hanan_nodes.index(x1)
                x_second_hanan_index = x_hanan_nodes.index(x2)
                y_first_hanan_index = y_hanan_nodes.index(y1)
                y_second_hanan_index = y_hanan_nodes.index(y2)
                min_distance = 999
                node_p = None
                for x_hanan in itertools.islice(x_hanan_nodes , min(x_first_hanan_index, x_second_hanan_index), max(x_first_hanan_index, x_second_hanan_index) + 1):
                    for y_hanan in itertools.islice(y_hanan_nodes , min(y_first_hanan_index, y_second_hanan_index), max(y_first_hanan_index, y_second_hanan_index) + 1):
                        if (x_hanan, y_hanan) not in nodes.values():
                            current_node_p = (x_hanan, y_hanan)
                            current_distance = compute_distance(current_node_p, current_node)
                            if min_distance > current_distance:
                                min_distance = current_distance
                                node_p = current_node_p
                if node_p:
                    nodes[-1] = node_p
                    adjacent_nodes_dict[-1] = [edge.keys()[0], edge.keys()[1]]
                    longest_edge = find_longest_edge_in_cycle(nodes, -1, node, adjacent_nodes_dict, edge.keys())

                    current_gain = compute_gain(nodes[longest_edge[0]], nodes[longest_edge[1]], node_p, current_node)
                    if best_gain < current_gain:
                        best_gain = current_gain
                        best_node = node
                        best_node_p = node_p
                        edge_to_remove = longest_edge
                    del nodes[-1]
                    del adjacent_nodes_dict[-1]
        if(best_gain > 0):
            gain_list.append((edge, best_node, best_node_p, edge_to_remove, best_gain))
    
    gain_list.sort(key=lambda element: -element[4])
    
    for item in gain_list:
        edge = (item[0].keys()[0], item[0].keys()[1])
        edge_to_remove = (item[3][0], item[3][1])
        if (edge_to_remove in graph.edges() or (edge_to_remove[1],edge_to_remove[0]) in graph.edges()) and (edge in graph.edges() or (edge[1],edge[0]) in graph.edges()):
            best_node = item[1]
            node_p = item[2]
            edge_to_remove = item[3]
            index_of_p = index_of_next_node
            graph.add_node(index_of_p, node_position = (node_p[0], node_p[1]), node_color="green")
            adjacent_nodes_dict[index_of_p] = []
            nodes[index_of_next_node] = (node_p[0], node_p[1])
            index_of_next_node += 1
            remove_edge(edge_to_remove[0], edge_to_remove[1], adjacent_nodes_dict)
            remove_edge(edge[0], edge[1], adjacent_nodes_dict)
            
            add_edge(edge[1], index_of_p, adjacent_nodes_dict)
            add_edge(edge[0], index_of_p, adjacent_nodes_dict)
            add_edge(index_of_p, best_node, adjacent_nodes_dict)

            show_graph()

def add_edge(node_id_1, node_id_2, adjacent_nodes_dict):
    graph.add_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].append(node_id_2)
    adjacent_nodes_dict[node_id_2].append(node_id_1)

def remove_edge(node_id_1, node_id_2, adjacent_nodes_dict):
    graph.remove_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].remove(node_id_2)
    adjacent_nodes_dict[node_id_2].remove(node_id_1)

def compute_distance(node_a, node_b):
    return math.fabs(node_b[0] - node_a[0]) + math.fabs(node_b[1] - node_a[1])

def compute_gain(node_a_of_edge_to_remove, node_b_of_edge_to_remove, new_node_p, node_of_pair):
    return compute_distance(node_a_of_edge_to_remove, node_b_of_edge_to_remove) - compute_distance(new_node_p, node_of_pair)

def find_longest_edge_in_cycle(nodes, node_1, node_2, adjacent_nodes_dict, considerated_edge):
    edges = find_path_node1_to_node2(node_1, node_2, adjacent_nodes_dict, [], considerated_edge)
    longest_edge = None
    longest_distance = 0
    for edge in edges:
        current_distance = compute_distance(nodes[edge[0]], nodes[edge[1]])
        if longest_distance < current_distance:
            longest_distance = current_distance
            longest_edge = edge
    return (longest_edge[0], longest_edge[1]) 

def find_path_node1_to_node2(node_1, node_2, adjacent_nodes_dict, edges, considerated_edge):
    if node_2 in adjacent_nodes_dict[node_1]:
        edge = (node_1, node_2)
        edges.append(edge)
        return edges
    else:
        for node in adjacent_nodes_dict[node_1]:
            if len(edges) is 0 or node is not edges[-1][0]:
                edge = (node_1, node)
                if not is_same_edge(edge, considerated_edge):
                    edges.append(edge)
                    edges_to_return = find_path_node1_to_node2(node, node_2, adjacent_nodes_dict, edges, considerated_edge)
                    if edges_to_return is not None:
                        return edges_to_return
                    else:
                        del edges[-1]
    return None

def is_same_edge(edge, considerated_edge):
    return (edge[0] is considerated_edge[0] and edge[1] is considerated_edge[1]) or (edge[1] is considerated_edge[0] and edge[0] is considerated_edge[1])

def compute_wirelength(nodes):
    wirelength = 0
    for edge in graph.edges():
        wirelength = wirelength + compute_distance(nodes[edge[0]], nodes[edge[1]])
    return wirelength

def recti_linearize_edge(x1, y1, x2, y2, node_id_1, node_id_2, biggest_node_id):
    biggest_node_id = biggest_node_id + 1
    graph.add_node(biggest_node_id, node_position = (x1, y2), node_color="blue")
    graph.remove_edge(node_id_1, node_id_2)
    graph.add_edge(node_id_1, biggest_node_id)
    graph.add_edge(biggest_node_id, node_id_2)

def recti_linearize_graph(nodes, biggest_node_id):
    edges = copy.deepcopy(graph.edges())
    for edge in edges:
        x1 = nodes[edge[0]][0]
        y1 = nodes[edge[0]][1]
        x2 = nodes[edge[1]][0]
        y2 = nodes[edge[1]][1]
        if not (x1 is x2 or y1 is y2):
            recti_linearize_edge(x1, y1, x2, y2, edge[0], edge[1], biggest_node_id) 
            biggest_node_id = biggest_node_id + 1   

if check_for_input_errors():
    begining_timestamp = current_milli_time()
    graph = nx.Graph()
    pointsFile = open("Points/"+sys.argv[1], "r")
    nodes = []
    graph_matrix = []
    adjacent_nodes_dict = {}
    for index, line in enumerate(pointsFile):
        pos_x, pos_y = [int(x) for x in line.split()]
        graph.add_node(index, node_position=(pos_x, pos_y), node_color="red")
        adjacent_nodes_dict[index] = []
        for node_id in nodes:
            x1 = graph.nodes[node_id]['node_position'][0]
            x2 = graph.nodes[index]['node_position'][0]
            y1 = graph.nodes[node_id]['node_position'][1]
            y2 = graph.nodes[index]['node_position'][1]
            distance_between_nodes = compute_distance((x1,y1), (x2,y2))
            graph_matrix.append([node_id, index, distance_between_nodes])
        nodes.append(index)
    
    if 'prim' == sys.argv[2].lower():
        mst_edges = prim.prims(len(nodes), graph_matrix)

    if 'kruskal' == sys.argv[2].lower():
        mst_edges = kruskal.kruskal(len(nodes), graph_matrix)
    
    for row in mst_edges:
        graph.add_edge(row[0], row[1])
        adjacent_nodes_dict[row[0]].append(row[1])
        adjacent_nodes_dict[row[1]].append(row[0])

    node_position = nx.get_node_attributes(graph,'node_position')
          
    list_of_hanan_nodes = []
    x_hanan_nodes = list(set([x[0] for x in node_position.values()]))
    y_hanan_nodes = list(set([y[1] for y in node_position.values()]))
    x_hanan_nodes.sort()
    y_hanan_nodes.sort()
    
    edges = []
    for mst_edge in mst_edges:
        edges.append({ mst_edge[0] : node_position[mst_edge[0]], mst_edge[1] : node_position[mst_edge[1]]})

    after_mst_timestamp = current_milli_time()
    wirelength_before = compute_wirelength(node_position)
    find_best_node_edge_pairs(edges, node_position, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict)
    wirelength_after = compute_wirelength(node_position)
    end_timestamp = current_milli_time()
    node_position = nx.get_node_attributes(graph,'node_position')
    
    recti_linearize_graph(node_position, len(x_hanan_nodes) * len(y_hanan_nodes) + len(node_position))
    show_graph()

    mst_time = after_mst_timestamp - begining_timestamp
    borah_time = end_timestamp - after_mst_timestamp

    print "MST Duration: " +str(mst_time)
    print "Borah Duration: " +str(borah_time)
    print "Wirelength before: " + str(wirelength_before)
    print "Wirelength after: " + str(wirelength_after)
    plt.show()
    

    