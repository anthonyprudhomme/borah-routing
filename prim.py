
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

def prims(vertices_number, graph_matrix):
  
  # create adj matrix from graph
  adjMatrix = createAdjMatrix(vertices_number, graph_matrix)
  
  # arbitrarily choose initial vertex from graph
  vertex = 0
  
  # initialize empty edges array and empty MST
  MST = []
  edges = []
  visited = []
  minEdge = [None,None,float('inf')]
  
  # run prims algorithm until we create an MST
  # that contains every vertex from the graph
  while len(MST) != vertices_number-1:
    
    # mark this vertex as visited
    visited.append(vertex)
    
    # add each edge to list of potential edges
    for r in range(0, vertices_number):
      if adjMatrix[vertex][r] != 0:
        edges.append([vertex,r,adjMatrix[vertex][r]])
        
    # find edge with the smallest weight to a vertex
    # that has not yet been visited
    for e in range(0, len(edges)):
      if edges[e][2] < minEdge[2] and edges[e][1] not in visited:
        minEdge = edges[e]
        
    # remove min weight edge from list of edges
    edges.remove(minEdge)

    # push min edge to MST
    MST.append(minEdge)
      
    # start at new vertex and reset min edge
    vertex = minEdge[1]
    minEdge = [None,None,float('inf')]
    
  return MST


def default_prim():
  
    # graph vertices are actually represented as numbers
    # like so: 0, 1, 2, ... V-1
    a, b, c, d, e, f = 0, 1, 2, 3, 4, 5

    # graph edges with weights
    # diagram of graph is shown above
    graph_matrix = [
    [a,b,2],
    [a,c,3],
    [b,d,3],
    [b,c,5],
    [b,e,4],
    [c,e,4],
    [d,e,2],
    [d,f,3],
    [e,f,5]
    ]
    # pass the # of vertices and the graph to run prims algorithm 
    print prims(6, graph_matrix)  