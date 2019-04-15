import itertools

import networkx as nx

import utils

def borah(edges, nodes, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict, graph, plot, show_progress, index_of_next_node):
    gain_list = []
    # Iterates over each edge
    for edge in edges:
        best_gain = 0
        best_node = None
        best_node_p = None
        node_p = None
        edge_to_remove = None
        # Iterates over each node in the graph (makes a pair node, edge) 
        for node in nodes:
            current_node = nodes[node]
            # Makes sure that the current node isn't part of the current edge
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
                # Get the few Hanan points from the rectilinear layout of the current edge
                for x_hanan in itertools.islice(x_hanan_nodes , min(x_first_hanan_index, x_second_hanan_index), max(x_first_hanan_index, x_second_hanan_index) + 1):
                    for y_hanan in itertools.islice(y_hanan_nodes , min(y_first_hanan_index, y_second_hanan_index), max(y_first_hanan_index, y_second_hanan_index) + 1):
                        # Makes sure that the point is not one of the nodes
                        if (x_hanan, y_hanan) not in nodes.values():
                            current_node_p = (x_hanan, y_hanan)
                            current_distance = utils.compute_distance(current_node_p, current_node)
                            # Finds the best node_p i.e. the hanan point that's the closest to the current node
                            if min_distance > current_distance:
                                min_distance = current_distance
                                node_p = current_node_p
                
                # If a node_p was found from the previous step
                if node_p:
                    # Temporary adds the node p to the list of nodes in order to compute the longest_edge
                    nodes[-1] = node_p
                    adjacent_nodes_dict[-1] = [edge.keys()[0], edge.keys()[1]]
                    longest_edge = utils.find_longest_edge_in_cycle(nodes, -1, node, adjacent_nodes_dict, edge.keys())
                    current_gain = utils.compute_gain(nodes[longest_edge[0]], nodes[longest_edge[1]], node_p, current_node)
                    del nodes[-1]
                    del adjacent_nodes_dict[-1]
                    # If the gain is better, keeps it
                    if best_gain < current_gain:
                        best_gain = current_gain
                        best_node = node
                        best_node_p = node_p
                        edge_to_remove = longest_edge
        # If the gain is positive then add it to the gain list        
        if(best_gain > 0):
            gain_list.append((edge, best_node, best_node_p, edge_to_remove, best_gain))
    
    # Sorts the gain list based on the gain
    gain_list.sort(key=lambda element: -element[4])
    
    # For each pair in the list, add the steiner point if possible
    for item in gain_list:
        edge = (item[0].keys()[0], item[0].keys()[1])
        edge_to_remove = (item[3][0], item[3][1])
        # Makes sure the steiner point can be added by checking if the edges to be removed are still in the graph
        if (edge_to_remove in graph.edges() or (edge_to_remove[1],edge_to_remove[0]) in graph.edges()) and (edge in graph.edges() or (edge[1],edge[0]) in graph.edges()):
            best_node = item[1]
            node_p = item[2]
            edge_to_remove = item[3]
            index_of_p = index_of_next_node
            # Adds node p
            graph.add_node(index_of_p, node_position = (node_p[0], node_p[1]), node_color="green")
            adjacent_nodes_dict[index_of_p] = []
            nodes[index_of_next_node] = (node_p[0], node_p[1])
            index_of_next_node += 1
            # Removes edge e2
            utils.remove_edge(edge_to_remove[0], edge_to_remove[1], adjacent_nodes_dict, graph)
            # Removes edge e1
            utils.remove_edge(edge[0], edge[1], adjacent_nodes_dict, graph)
            
            # Adds edge from p to node 1 of the edge in the pair
            utils.add_edge(edge[0], index_of_p, adjacent_nodes_dict, graph)
            # Adds edge from p to node 2 of the edge in the pair
            utils.add_edge(edge[1], index_of_p, adjacent_nodes_dict, graph)
            # Adds edge from p to node in the pair
            utils.add_edge(index_of_p, best_node, adjacent_nodes_dict, graph)

            # Shows the progress animation if the user gave this parameter
            if show_progress:
                utils.show_graph(plot, graph)
    
    return index_of_next_node