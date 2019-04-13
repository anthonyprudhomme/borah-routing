import sys

import math
import itertools
import time
import copy
import argparse

# Graph and plot imports
import matplotlib.pyplot as plot
import networkx as nx

# Local imports
import prim
import kruskal
import borah
import utils

current_milli_time = lambda: int(round(time.time() * 1000))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Borah routing project by Guillaume Guerin and Anthony Prudhomme", epilog="Example Usages:\npython main.py --input points_10_5.pts.txt --mst_alg prim --num_pass 10 --show_progress")
    parser.add_argument('-i', '--input', help="Input points file.", required=True)
    parser.add_argument('-mst', '--mst_alg', help="Minimum spanning tree algorithm.", required=True, choices=["prim", "kruskal"])
    parser.add_argument('-pass', '--num_pass', help="Number of pass you want to run.")
    parser.add_argument('-prog', '--show_progress', help="Shows an updated graph for each new added Steiner point. /!\ Performance will be highly degraded in that case. /!\ ", action='store_true')
    args = parser.parse_args()

    begining_timestamp = current_milli_time()
    # Create the graph with no node
    graph = nx.Graph()
    # Loads the points file
    pointsFile = open("Points/"+args.input, "r")
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
            distance_between_nodes = utils.compute_distance((x1,y1), (x2,y2))
            graph_matrix.append([node_id, index, distance_between_nodes])
        nodes.append(index)
    
    if 'prim' == args.mst_alg:
        mst_edges = prim.prim(len(nodes), graph_matrix)

    if 'kruskal' == args.mst_alg:
        mst_edges = kruskal.kruskal(len(nodes), graph_matrix)
    
    edges = []
    node_position = nx.get_node_attributes(graph,'node_position')
    for row in mst_edges:
        graph.add_edge(row[0], row[1])
        adjacent_nodes_dict[row[0]].append(row[1])
        adjacent_nodes_dict[row[1]].append(row[0])
        edges.append({ row[0] : node_position[row[0]], row[1] : node_position[row[1]]})
        
    list_of_hanan_nodes = []
    x_hanan_nodes = list(set([x[0] for x in node_position.values()]))
    y_hanan_nodes = list(set([y[1] for y in node_position.values()]))
    x_hanan_nodes.sort()
    y_hanan_nodes.sort()

    after_mst_timestamp = current_milli_time()
    wirelength_before = utils.compute_wirelength(node_position, graph)
    # Run borah routing
    borah.find_best_node_edge_pairs(edges, node_position, x_hanan_nodes, y_hanan_nodes, adjacent_nodes_dict, graph, plot, args.show_progress)
    wirelength_after = utils.compute_wirelength(node_position, graph)
    end_timestamp = current_milli_time()
    node_position = nx.get_node_attributes(graph,'node_position')
    
    utils.recti_linearize_graph(node_position, len(x_hanan_nodes) * len(y_hanan_nodes) + len(node_position), graph)
    utils.show_graph(plot, graph)

    mst_time = after_mst_timestamp - begining_timestamp
    borah_time = end_timestamp - after_mst_timestamp

    print ("MST Duration: " +str(mst_time))
    print ("Borah Duration: " +str(borah_time))
    print ("Wirelength before: " + str(wirelength_before))
    print ("Wirelength after: " + str(wirelength_after))
    plot.show()
    

    