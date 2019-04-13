
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

def prim(vertices_number, graph_matrix):
  
  # create adj matrix from graph
  adjMatrix = createAdjMatrix(vertices_number, graph_matrix)
  
  # arbitrarily choose initial vertex from graph
  vertex = 0
  
  # initialize empty edges array and empty MST
  mst = []
  edges = []
  visited = []
  min_edge = [None,None,float('inf')]
  
  # run prims algorithm until we create an MST
  # that contains every vertex from the graph
  while len(mst) != vertices_number-1:
    
    # mark this vertex as visited
    visited.append(vertex)
    
    # add each edge to list of potential edges
    for r in range(0, vertices_number):
      if adjMatrix[vertex][r] != 0:
        edges.append([vertex,r,adjMatrix[vertex][r]])
        
    # find edge with the smallest weight to a vertex
    # that has not yet been visited
    for edge in range(0, len(edges)):
      if edges[edge][2] < min_edge[2] and edges[edge][1] not in visited:
        min_edge = edges[edge]
        
    # remove min weight edge from list of edges
    edges.remove(min_edge)

    # push min edge to MST
    mst.append(min_edge)
      
    # start at new vertex and reset min edge
    vertex = min_edge[1]
    min_edge = [None,None,float('inf')]
  return mst