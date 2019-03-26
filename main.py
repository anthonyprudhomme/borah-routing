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

def find_best_node_edge_pairs(edges, nodes, x_hanan_nodes, y_hanan_nodes):
    index_of_next_node = len(x_hanan_nodes) * len(y_hanan_nodes)
    for edge in edges:
        best_gain = 0
        best_node = None
        node_p = None
        node_p2 = None
        edge_to_remove = None
        for node in nodes:
            if not (edge.values()[0] is node or edge.values()[1] is node):
                x1 = edge.values()[0][0]
                y1 = edge.values()[0][1]
                x2 = edge.values()[1][0]
                y2 = edge.values()[1][1]
                print(y_hanan_nodes)
                print(x_hanan_nodes)
                x_first_hanan_index = x_hanan_nodes.index(x1)
                x_second_hanan_index = x_hanan_nodes.index(x2)
                y_first_hanan_index = y_hanan_nodes.index(y1)
                y_second_hanan_index = y_hanan_nodes.index(y2)
                
                for x_hanan in itertools.islice(x_hanan_nodes , min(x_first_hanan_index, x_second_hanan_index), max(x_first_hanan_index, x_second_hanan_index)):
                    for y_hanan in itertools.islice(y_hanan_nodes , min(y_first_hanan_index, y_second_hanan_index), max(y_first_hanan_index, y_second_hanan_index)):
                        if [x_hanan, y_hanan] not in nodes.values():
                            
                            node_p = [x_hanan, y_hanan]
                            if x_hanan is x1:
                                node_p2 = [x1, y2]
                            elif x_hanan is x2:
                                node_p2 = [x2, y1]
                            elif y_hanan is y1:
                                node_p2 = [x2, y1]
                            else:
                                node_p2 = [x1, y2]
                            graph.add_node(-1, node_position = (node_p[0], node_p[1]))
                            index_of_next_node += 1
                            graph.add_node(-2, node_position = (node_p2[0], node_p2[1]))
                            index_of_next_node += 1
                            graph.remove_edge(edge_to_remove)
                            graph.remove_edge(edge)
                            # There might be a mistake here because there is no edge between edge[0] (i) or edge[1] (j) and p
                            graph.add_edge(edge[0], node_p2)
                            graph.add_edge(best_node, node_p)
                            graph.add_edge(edge[1], node_p2)
                            longest_edge = find_longest_edge_in_cycle()

                            current_gain = compute_gain(longest_edge[0], longest_edge[1], [x_hanan, y_hanan], node)
                            if best_gain < current_gain:
                                best_gain = current_gain
                                best_node = node
                                edge_to_remove = longest_edge
        if(best_gain > 0):
            graph.add_node(index_of_next_node, node_position = (node_p[0], node_p[1]))
            index_of_next_node += 1
            graph.add_node(index_of_next_node, node_position = (node_p2[0], node_p2[1]))
            index_of_next_node += 1
            graph.remove_edge(edge_to_remove)
            graph.remove_edge(edge)
            # There might be a mistake here because there is no edge between edge[0] (i) or edge[1] (j) and p
            graph.add_edge(edge[0], node_p2)
            graph.add_edge(best_node, node_p)
            graph.add_edge(edge[1], node_p2)
        

def compute_distance(node_a, node_b):
    return math.fabs(node_b[0] - node_a[0]) + math.fabs(node_b[1] - node_a[1])

def compute_gain(node_a_of_edge_to_remove, node_b_of_edge_to_remove, new_node_p, node_of_pair):
    return compute_distance(node_a_of_edge_to_remove, node_b_of_edge_to_remove) - compute_distance(new_node_p, node_of_pair)

def find_longest_edge_in_cycle():
    try:
        cycle = list(nx.find_cycle(G, orientation='ignore'))
        longest_edge = None
        longest_distance = 0
        for edge in cycle:
            current_distance = compute_distance(edge[0], edge[1])
            if longest_distance < current_distance:
                longest_distance = current_distance
                longest_edge = edge
        return longest_edge
    except:
        pass
    return None

if check_for_input_errors():
    graph = nx.Graph()
    pointsFile = open("Points/"+sys.argv[1], "r")
    nodes = []
    graph_matrix = []
    for index, line in enumerate(pointsFile):
        pos_x, pos_y = [int(x) for x in line.split()]
        graph.add_node(index, node_position=(pos_x, pos_y))
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
        for row in mst_edges:
            graph.add_edge(row[0], row[1])

    if 'kruskal' == sys.argv[2].lower():
        mst_edges = kruskal.kruskal(len(nodes), graph_matrix)
        for row in mst_edges:
            graph.add_edge(row[0], row[1])
    
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
    for i in range(len(list_of_hanan_nodes) + len(node_position)):
        if i < len(node_position):
            color_map.append('red')
        else:
            color_map.append('green')
    hanan_node_position = nx.get_node_attributes(graph, 'node_position')        
    nx.draw(graph, hanan_node_position, node_color = color_map, with_labels=True, font_weight='bold')
    edges = []
    for mst_edge in mst_edges:
        edges.append({ mst_edge[0] : node_position[mst_edge[0]], mst_edge[1] : node_position[mst_edge[1]]})
    x_hanan_nodes.sort()
    y_hanan_nodes.sort()
    find_best_node_edge_pairs(edges, node_position, x_hanan_nodes, y_hanan_nodes)

    plt.show()
    

    