import copy
import math

import networkx as nx

# Computes the Manhattan distance between two nodes
def compute_distance(node_a, node_b):
    return math.fabs(node_b[0] - node_a[0]) + math.fabs(node_b[1] - node_a[1])

# Computes the gain
def compute_gain(node_a_of_edge_to_remove, node_b_of_edge_to_remove, new_node_p, node_of_pair):
    return compute_distance(node_a_of_edge_to_remove, node_b_of_edge_to_remove) - compute_distance(new_node_p, node_of_pair)

# Finds the longest edge in the cycle and returns it
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

# Finds the list of edges that link from one node to an other 
def find_path_node1_to_node2(node_1, node_2, adjacent_nodes_dict, edges, considered_edge):
    if node_2 in adjacent_nodes_dict[node_1]:
        edge = (node_1, node_2)
        edges.append(edge)
        return edges
    else:
        for node in adjacent_nodes_dict[node_1]:
            if len(edges) is 0 or node is not edges[-1][0]:
                edge = (node_1, node)
                if not is_same_edge(edge, considered_edge):
                    edges.append(edge)
                    edges_to_return = find_path_node1_to_node2(node, node_2, adjacent_nodes_dict, edges, considered_edge)
                    if edges_to_return is not None:
                        return edges_to_return
                    else:
                        del edges[-1]
    return None

# Returns a boolean checking if the two edges are the same
def is_same_edge(edge, considered_edge):
    return (edge[0] is considered_edge[0] and edge[1] is considered_edge[1]) or (edge[1] is considered_edge[0] and edge[0] is considered_edge[1])

# Display the graph at its current state for 0.5s
def show_graph(plot, graph):
    node_position = nx.get_node_attributes(graph,'node_position')
    color_map = nx.get_node_attributes(graph,'node_color').values()
    nx.draw(graph, node_position, with_labels=True, node_color=color_map, font_weight='bold', node_size = 100, font_size=5)
    plot.draw()
    plot.pause(0.5)
    plot.clf()

# Computes the wirelength of the graph
def compute_wirelength(nodes, graph):
    wirelength = 0
    for edge in graph.edges():
        wirelength = wirelength + compute_distance(nodes[edge[0]], nodes[edge[1]])
    return wirelength

# Recti-linearizes an edge
def recti_linearize_edge(x1, y1, x2, y2, node_id_1, node_id_2, biggest_node_id, graph):
    biggest_node_id = biggest_node_id + 1
    graph.add_node(biggest_node_id, node_position = (x1, y2), node_color="blue")
    graph.remove_edge(node_id_1, node_id_2)
    graph.add_edge(node_id_1, biggest_node_id)
    graph.add_edge(biggest_node_id, node_id_2)

# Recti-linearizes the graph
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

# Adds an edge and update the dict of adjacent nodes
def add_edge(node_id_1, node_id_2, adjacent_nodes_dict, graph):
    graph.add_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].append(node_id_2)
    adjacent_nodes_dict[node_id_2].append(node_id_1)

# Removes an edge and update the dict of adjacent nodes
def remove_edge(node_id_1, node_id_2, adjacent_nodes_dict, graph):
    graph.remove_edge(node_id_1, node_id_2)
    adjacent_nodes_dict[node_id_1].remove(node_id_2)
    adjacent_nodes_dict[node_id_2].remove(node_id_1)