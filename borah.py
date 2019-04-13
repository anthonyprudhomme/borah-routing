import itertools

import networkx as nx

import utils

def find_best_node_edge_pairs(edges, nodes, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict, graph, plot, show_progress):
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
                            current_distance = utils.compute_distance(current_node_p, current_node)
                            if min_distance > current_distance:
                                min_distance = current_distance
                                node_p = current_node_p
                if node_p:
                    nodes[-1] = node_p
                    adjacent_nodes_dict[-1] = [edge.keys()[0], edge.keys()[1]]
                    longest_edge = utils.find_longest_edge_in_cycle(nodes, -1, node, adjacent_nodes_dict, edge.keys())

                    current_gain = utils.compute_gain(nodes[longest_edge[0]], nodes[longest_edge[1]], node_p, current_node)
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
            utils.remove_edge(edge_to_remove[0], edge_to_remove[1], adjacent_nodes_dict, graph)
            utils.remove_edge(edge[0], edge[1], adjacent_nodes_dict, graph)
            
            utils.add_edge(edge[1], index_of_p, adjacent_nodes_dict, graph)
            utils.add_edge(edge[0], index_of_p, adjacent_nodes_dict, graph)
            utils.add_edge(index_of_p, best_node, adjacent_nodes_dict, graph)

            if show_progress:
                utils.show_graph(plot, graph)