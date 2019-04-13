import copy
import math

import networkx as nx

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


def show_graph(plot, graph):
    node_position = nx.get_node_attributes(graph,'node_position')
    color_map = nx.get_node_attributes(graph,'node_color').values()
    nx.draw(graph, node_position, with_labels=True, node_color=color_map, font_weight='bold')
    plot.draw()
    plot.pause(1)
    plot.clf()

def compute_wirelength(nodes, graph):
    wirelength = 0
    for edge in graph.edges():
        wirelength = wirelength + compute_distance(nodes[edge[0]], nodes[edge[1]])
    return wirelength

def recti_linearize_edge(x1, y1, x2, y2, node_id_1, node_id_2, biggest_node_id, graph):
    biggest_node_id = biggest_node_id + 1
    graph.add_node(biggest_node_id, node_position = (x1, y2), node_color="blue")
    graph.remove_edge(node_id_1, node_id_2)
    graph.add_edge(node_id_1, biggest_node_id)
    graph.add_edge(biggest_node_id, node_id_2)

def recti_linearize_graph(nodes, biggest_node_id, graph):
    edges = copy.deepcopy(graph.edges())
    for edge in edges:
        x1 = nodes[edge[0]][0]
        y1 = nodes[edge[0]][1]
        x2 = nodes[edge[1]][0]
        y2 = nodes[edge[1]][1]
        if not (x1 is x2 or y1 is y2):
            recti_linearize_edge(x1, y1, x2, y2, edge[0], edge[1], biggest_node_id, graph) 
            biggest_node_id = biggest_node_id + 1   

def add_edge(node_id_1, node_id_2, adjacent_nodes_dict, graph):
    graph.add_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].append(node_id_2)
    adjacent_nodes_dict[node_id_2].append(node_id_1)

def remove_edge(node_id_1, node_id_2, adjacent_nodes_dict, graph):
    graph.remove_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].remove(node_id_2)
    adjacent_nodes_dict[node_id_2].remove(node_id_1)