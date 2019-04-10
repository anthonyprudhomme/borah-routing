import sys

import matplotlib.pyplot as plt
import networkx as nx
import prim
import kruskal
import math
import itertools

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

def find_overlaping_edge(key, edge, p2, adjacent_nodes_dict, nodes):
    for node in adjacent_nodes_dict[key]:
        node_position = nodes[node]
        x_is_same = False
        y_is_same = False
        if p2[0] is edge[0]:
            x_is_same = True
        if p2[1] is edge[1]:
            y_is_same = True
        if x_is_same and edge[0] is node_position[0]:
            return True
        if y_is_same and edge[1] is node_position[1]:
            return True
        return False

def find_best_node_edge_pairs(edges, nodes, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict):
    index_of_next_node = len(x_hanan_nodes) * len(y_hanan_nodes)
    for edge in edges:
        if edge.keys() in graph.edges():
            print ("******=====NEW EDGE=====******")
            best_gain = 0
            best_node = None
            node_p = None
            node_p2 = None
            edge_to_remove = None
            final_e1_to_p = False
            for node in nodes:
                current_node = nodes[node]
                print "--------NEW NODE: "+ str(node) + " " + str(current_node) +"---------"
                print "Current edge:" + str(edge)
                if not (edge.values()[0] is current_node or edge.values()[1] is current_node):
                    edge_1 = edge.values()[0]
                    edge_2 = edge.values()[1]
                    x1 = edge_1[0]
                    y1 = edge_1[1]
                    x2 = edge_2[0]
                    y2 = edge_2[1]
                    x_first_hanan_index = x_hanan_nodes.index(x1)
                    x_second_hanan_index = x_hanan_nodes.index(x2)
                    x_third_hanan_index = x_hanan_nodes.index(current_node[0])
                    y_first_hanan_index = y_hanan_nodes.index(y1)
                    y_second_hanan_index = y_hanan_nodes.index(y2)
                    y_third_hanan_index = y_hanan_nodes.index(current_node[1])
                    for x_hanan in itertools.islice(x_hanan_nodes , min(x_first_hanan_index, x_second_hanan_index, x_third_hanan_index), max(x_first_hanan_index, x_second_hanan_index, x_third_hanan_index) + 1):
                        for y_hanan in itertools.islice(y_hanan_nodes , min(y_first_hanan_index, y_second_hanan_index, y_third_hanan_index), max(y_first_hanan_index, y_second_hanan_index, y_third_hanan_index) + 1):
                            if (x_hanan, y_hanan) not in nodes.values():
                                e1_to_p = False
                                e2_to_p = False
                                node_p = (x_hanan, y_hanan)
                                if x1 is x2 or y1 is y2:
                                    node_p2 = node_p
                                    e1_to_p = True
                                else:
                                    if x_hanan is x1:
                                        node_p2 = [x1, y2]
                                        e1_to_p = True
                                    elif x_hanan is x2:
                                        node_p2 = [x2, y1]
                                        e2_to_p = True
                                    elif y_hanan is y1:
                                        node_p2 = [x2, y1]
                                        e1_to_p = True
                                    else:
                                        node_p2 = [x1, y2]
                                        e2_to_p = True
                                graph.add_node(-1, node_position = (node_p[0], node_p[1]))
                                graph.add_node(-2, node_position = (node_p2[0], node_p2[1]))

                                if e1_to_p:
                                    graph.add_edge(edge.keys()[0], -1)
                                    graph.add_edge(edge.keys()[1], -2)
                                if e2_to_p:
                                    graph.add_edge(edge.keys()[1], -1)
                                    graph.add_edge(edge.keys()[0], -2)
                                graph.add_edge(-1, -2)
                                graph.add_edge(-1, node)

                                # overlap_edge_1 = find_overlaping_edge(edge.keys()[0], edge_1, node_p2, adjacent_nodes_dict, nodes)
                                # overlap_edge_2 = find_overlaping_edge(edge.keys()[1], edge_2, node_p2, adjacent_nodes_dict, nodes)
                                # if overlap_edge_1:
                                #     graph.add_edge(edge[0], -2)
                                # if overlap_edge_2:
                                #      graph.add_edge(edge[1], -2)
                                # graph.add_edge(node, -1)
                                nodes[-1] = node_p
                                nodes[-2] = node_p2
                                print graph.edges()
                                graph.remove_edge(edge.keys()[0], edge.keys()[1])
                                longest_edge = find_longest_edge_in_cycle(nodes, edge)
                                print "Longest edge: " + str(longest_edge)
                                if e1_to_p:
                                    graph.remove_edge(edge.keys()[0], -1)
                                    graph.remove_edge(edge.keys()[1], -2)
                                if e2_to_p:
                                    graph.remove_edge(edge.keys()[1], -1)
                                    graph.remove_edge(edge.keys()[0], -2)
                                graph.remove_edge(-1, -2)
                                graph.remove_edge(-1, node)
                                graph.remove_node(-1)
                                graph.remove_node(-2)
                                graph.add_edge(edge.keys()[0], edge.keys()[1])

                                current_gain = compute_gain(nodes[longest_edge[0]], nodes[longest_edge[1]], (x_hanan, y_hanan), current_node)
                                if best_gain < current_gain:
                                    print "New best gain: " + str(current_gain)
                                    print str(nodes[longest_edge[0]])
                                    print str(nodes[longest_edge[1]])
                                    print (x_hanan, y_hanan)
                                    print (current_node)
                                    print "Node p: "+ str(node_p) + " node_p2: "+ str(node_p2)
                                    best_gain = current_gain
                                    best_node = node
                                    edge_to_remove = longest_edge
                                    final_e1_to_p = e1_to_p
                                del nodes[-1]
                                del nodes[-2]
                    print "---------END OF NODE----------"
            if(best_gain > 0):
                print "======Result======"
                print "Best gain: " + str(best_gain)
                print str(best_node) + " " + str(nodes[best_node])
                print "Removed edge: " + str(edge_to_remove)
                print adjacent_nodes_dict

                index_of_p = index_of_next_node
                graph.add_node(index_of_p, node_position = (node_p[0], node_p[1]))
                nodes[index_of_next_node] = (node_p[0], node_p[1])
                index_of_next_node += 1
                index_of_p2 = index_of_next_node

                graph.add_node(index_of_p2, node_position = (node_p2[0], node_p2[1]))
                nodes[index_of_next_node] = (node_p2[0], node_p2[1])
                index_of_next_node += 1

                graph.remove_edge(edge_to_remove[0], edge_to_remove[1])
                graph.remove_edge(edge.keys()[0], edge.keys()[1])
            
                if final_e1_to_p:
                    graph.add_edge(edge.keys()[0], index_of_p)
                    graph.add_edge(edge.keys()[1], index_of_p2)
                else:
                    graph.add_edge(edge.keys()[1], index_of_p2)
                    graph.add_edge(edge.keys()[0], index_of_p)
                graph.add_edge(index_of_p, index_of_p2)
                graph.add_edge(index_of_p, best_node)

def compute_distance(node_a, node_b):
    return math.fabs(node_b[0] - node_a[0]) + math.fabs(node_b[1] - node_a[1])

def compute_gain(node_a_of_edge_to_remove, node_b_of_edge_to_remove, new_node_p, node_of_pair):
    return compute_distance(node_a_of_edge_to_remove, node_b_of_edge_to_remove) - compute_distance(new_node_p, node_of_pair)

def find_longest_edge_in_cycle(nodes, edge_to_keep):
    cycle = list(nx.find_cycle(graph, orientation='ignore'))
    print "Cycle: " + str(cycle)
    longest_edge = None
    longest_distance = 0
    for edge in cycle:
        # if (edge[0] is not edge_to_keep.keys()[0] or edge[1] is not edge_to_keep.keys()[1]) and (edge[1] is not edge_to_keep.keys()[0] or edge[0] is not edge_to_keep.keys()[1]):
        current_distance = compute_distance(nodes[edge[0]], nodes[edge[1]])
        # print str("Distance for: ") + str(current_distance) + " " + str(nodes[edge[0]]) + " " + str(edge[0]) + " "+ str(nodes[edge[1]]) + " "+ str(edge[1])
        # print "Current  distance: " + str(current_distance)
        if longest_distance < current_distance:
            longest_distance = current_distance
            longest_edge = edge
    return (longest_edge[0], longest_edge[1]) 

def find_path_p1_to_p2(p1, p2, adjacent_nodes_dict, edges):
    print "called " + str(p1)
    if p2 in adjacent_nodes_dict[p1]:
        edge = (p1, p2)
        edges.append(edge)
        return edges
    else:
        for node in adjacent_nodes_dict[p1]:
            if len(edges) is 0 or node is not edges[len(edges)-1][0]:
                edge = (p1, node)
                edges.append(edge)
                edges = find_path_p1_to_p2(node, p2, adjacent_nodes_dict, edges)
                if edges is not None:
                    return edges
    return None

if check_for_input_errors():
    graph = nx.Graph()
    pointsFile = open("Points/"+sys.argv[1], "r")
    nodes = []
    graph_matrix = []
    adjacent_nodes_dict = {}
    for index, line in enumerate(pointsFile):
        pos_x, pos_y = [int(x) for x in line.split()]
        graph.add_node(index, node_position=(pos_x, pos_y))
        adjacent_nodes_dict[index] = []
        for node_id in nodes:
            x1 = graph.nodes[node_id]['node_position'][0]
            x2 = graph.nodes[index]['node_position'][0]
            y1 = graph.nodes[node_id]['node_position'][1]
            y2 = graph.nodes[index]['node_position'][1]
            distance_between_nodes = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
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

    list_to_create_hanan = [] #list of nodes index in the MST

    node_position = nx.get_node_attributes(graph,'node_position')
          
    list_of_hanan_nodes = []
    x_hanan_nodes = []
    y_hanan_nodes = []
    for i in range(len(node_position)):
        for j in range(len(node_position)):
            if (i != j) and ((node_position[i][0],node_position[j][1]) not in node_position.values()) and ([node_position[i][0],node_position[j][1]] not in list_of_hanan_nodes):
                list_of_hanan_nodes.append([node_position[i][0],node_position[j][1]])
                if node_position[i][0] not in x_hanan_nodes:
                    x_hanan_nodes.append(node_position[i][0])
                if node_position[j][1] not in y_hanan_nodes:
                    y_hanan_nodes.append(node_position[j][1])
    
    #Now we will plot hanan node on the graph
    nbr_points_in_graph = len(node_position)
    hanan_nodes_position = {}
    for i in range(nbr_points_in_graph,nbr_points_in_graph+len(list_of_hanan_nodes)):
        hanan_nodes_position[i] = tuple(list_of_hanan_nodes[i-nbr_points_in_graph])
        graph.add_node(i, node_position=(hanan_nodes_position[i][0], hanan_nodes_position[i][1]))
    color_map = []
    
    edges = []
    for mst_edge in mst_edges:
        edges.append({ mst_edge[0] : node_position[mst_edge[0]], mst_edge[1] : node_position[mst_edge[1]]})
    x_hanan_nodes.sort()
    y_hanan_nodes.sort()

    find_best_node_edge_pairs(edges, node_position, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict)

    node_position = nx.get_node_attributes(graph,'node_position')
    for i in range(len(list_of_hanan_nodes) + len(node_position)):
        if i < nbr_points_in_graph:
            color_map.append('red')
        else:
            color_map.append('green')
    nx.draw(graph, node_position, with_labels=True, node_color=color_map, font_weight='bold')

    plt.show()
    

    