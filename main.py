import sys

import matplotlib.pyplot as plt
import networkx as nx
import prim
import kruskal
import math

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

if check_for_input_errors():
    graph = nx.Graph()
    pointsFile = open("Points/"+sys.argv[1], "r")
    nodes = []
    graph_matrix = []
    for index, line in enumerate(pointsFile):
        pos_x, pos_y = [int(x) for x in line.split()]
        graph.add_node(index, node_position=(pos_x, pos_y))
        print(index,(pos_x, pos_y))
        for node_id in nodes:
            x1 = graph.nodes[node_id]['node_position'][0]
            x2 = graph.nodes[index]['node_position'][0]
            y1 = graph.nodes[node_id]['node_position'][1]
            y2 = graph.nodes[index]['node_position'][1]
            distance_between_nodes = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            graph_matrix.append([node_id, index, distance_between_nodes])
        nodes.append(index)

    
    if 'prim' == sys.argv[2].lower():
        result = prim.prims(len(nodes), graph_matrix)
        for row in result:
            graph.add_edge(row[0], row[1])
        #MST = result #we will just use this list to exctract coordinates of all nodes belonging to the MST

    if 'kruskal' == sys.argv[2].lower():
        #list_to_create_hanan = result
        result = kruskal.kruskal(len(nodes), graph_matrix)
        for row in result:
            graph.add_edge(row[0], row[1])

    node_position=nx.get_node_attributes(graph,'node_position')
    #print(node_position)
    nx.draw(graph, node_position, with_labels=True, font_weight='bold')
    
    list_to_create_hanan = [] #list of nodes index in the MST
    
    
    #we build hanan matrix which contains x and y coordinates of all hanan node. Il me fallait juste extraire les coordonnees de tous les noeuds du graphes
    #Je sais pas pourquoi jai fait tout ca en fait. 
    hanan = []
    for i in range(len(result)):
        for j in range(2):
            if result[i][j] not in list_to_create_hanan: #to only add node index once, for instance if there is edge (4,0) and (0,2), we want to add 0 only once
                list_to_create_hanan.append(result[i][j])
    list_to_create_hanan.sort()
    print("list_to_create_hanan =")
    print(list_to_create_hanan)
    for node_id in nodes:
         if node_id in list_to_create_hanan:
            x = graph.nodes[node_id]['node_position'][0]
            y = graph.nodes[node_id]['node_position'][1]
            hanan.append([x,y])

    #print("hanan =")
    #print(hanan)        
          
    list_of_hanan_nodes = []
    for i in range(len(hanan)):
        for j in range(len(hanan)):
            if (i != j) and ([hanan[i][0],hanan[j][1]] not in hanan) and ([hanan[i][0],hanan[j][1]] not in list_of_hanan_nodes):
                list_of_hanan_nodes.append([hanan[i][0],hanan[j][1]])
    print("list_of_hanan_nodes =")            
    print(list_of_hanan_nodes)    
    #print("graph_matrix =")
    #print(graph_matrix)
    #print("result =")
    #print(result)
    
    
    #Now we will plot hanan node on the graph
    nbr_points_in_graph = len(list_to_create_hanan)
    hanan_nodes_position = {}
    for i in range(nbr_points_in_graph,nbr_points_in_graph+len(list_of_hanan_nodes)):
        hanan_nodes_position[i] = tuple(list_of_hanan_nodes[i-nbr_points_in_graph])
        print(hanan_nodes_position[i])
        graph.add_node(tuple([i,hanan_nodes_position[i]]))
    print("hanan_nodes_position =")
    print(hanan_nodes_position)
    node_position.update(hanan_nodes_position)
    print("la position de tous les noeuds est =")
    print(node_position)
    color_map = []
    for i in range(len(list_of_hanan_nodes) + len(list_to_create_hanan)):
        if i < len(list_to_create_hanan):
            color_map.append('red')
        else:
            color_map.append('green')
            
    #nx.draw(graph,node_position,node_color = color_map, with_labels=True, font_weight='bold')
    #nx.draw(hanan_nodes_position,node_color='b')
    
    
    
    plt.show()
    