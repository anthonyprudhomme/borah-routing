import sys

import matplotlib.pyplot as plt
import networkx as nx


graph = nx.Graph()
pointsFile = open("Points/"+sys.argv[1], "r")
nodes = []
for index, line in enumerate(pointsFile):
  pos_x, pos_y = [int(x) for x in line.split()]
  graph.add_node(index, node_position=(pos_x, pos_y))
  for node_id in nodes:
    graph.add_edge(index, node_id)
  nodes.append(index)

node_position=nx.get_node_attributes(graph,'node_position')
nx.draw(graph, node_position, with_labels=True, font_weight='bold')

plt.show()