import sys

import matplotlib.pyplot as plt
import networkx as nx
import prim
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
        for node_id in nodes:
            x1 = graph.nodes[node_id]['node_position'][0]
            x2 = graph.nodes[index]['node_position'][0]
            y1 = graph.nodes[node_id]['node_position'][1]
            y2 = graph.nodes[index]['node_position'][1]
            distance_between_nodes = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            graph_matrix.append([node_id, index, distance_between_nodes])
        nodes.append(index)

    
    if 'prim' == sys.argv[2].lower():
        prim_result = prim.prims(len(nodes), graph_matrix)
        for row in prim_result:
            graph.add_edge(row[0], row[1])

    if 'kruskal' == sys.argv[2].lower():
        print ('Not implemented yet')
        #kruskal_result = kruskal.kruskal(len(nodes), graph_matrix)
        #for row in kruskal_result:
        #    graph.add_edge(row[0], row[1])

    node_position=nx.get_node_attributes(graph,'node_position')
    nx.draw(graph, node_position, with_labels=True, font_weight='bold')

    plt.show()