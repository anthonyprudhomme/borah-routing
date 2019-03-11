def createAdjMatrix(vertices_number, graph_matrix):
  
  adjMatrix = []
  
  # create N x N matrix filled with 0 edge weights between all vertices
  for i in range(0, vertices_number):
    adjMatrix.append([])
    for j in range(0, vertices_number):
      adjMatrix[i].append(0)
      
  # populate adjacency matrix with correct edge weights
  for i in range(0, len(graph_matrix)):
    adjMatrix[graph_matrix[i][0]][graph_matrix[i][1]] = graph_matrix[i][2]
    adjMatrix[graph_matrix[i][1]][graph_matrix[i][0]] = graph_matrix[i][2]
    
  return adjMatrix

def kruskal(vertices_number,graph_matrix):
    # create adj matrix from graph
  adjMatrix = createAdjMatrix(vertices_number, graph_matrix)
  graph_matrix_sorted = copy.deepcopy(graph_matrix)
  graph_matrix_sorted.sort(key=lambda edge: edge[2])
  list_of_added_edges = []
  
  possible_paths = []
  while len(list_of_added_edges) < vertices_number-1:
      smallest_weighted_edge = graph_matrix_sorted.pop(0)
      first_path_index = -1
      second_path_index = -1
      for index, path in enumerate(possible_paths):
          if ((smallest_weighted_edge[0] in path) and (smallest_weighted_edge[1] in path)):
              ##A cycle has been created
          else:
              if (smallest_weighted_edge[0] in path):
                  first_path_index = index
              if (smallest_weighted_edge[1] in path):
                  second_path_index = index
                  
                  
       if first_path_index != -1 and second_path_index !=-1:
           #On fusionne nos 2 listes des possible_path
       else if first_path_index != -1:
           #On ajoute le noeud en question à la liste des possible path
       else if second_path_index !=-1:
           #On ajoute le noeud en question à la liste des possible path
       else:
           #Aucun des 2 noeuds n'appartient à un des possible_path deja existants,
           #on cree donc un nouveau possible path. Ce qui revient a creer un autre sous-graphe non-connecte

          