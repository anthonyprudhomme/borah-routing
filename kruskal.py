import copy

def kruskal(vertices_number, graph_matrix):
    graph_matrix_sorted = copy.deepcopy(graph_matrix)
    graph_matrix_sorted.sort(key=lambda edge: edge[2]) # its graph matrix where lines are sorted from the shortest distance between 2 nodes to the longest
    list_of_added_edges = [] #we build MST by adding nodes 1 by 1
    possible_paths = [] #list of all nodes linked together forming a "possible path"
    while len(list_of_added_edges) < vertices_number-1:
        smallest_weighted_edge = graph_matrix_sorted.pop(0)
        first_path_index = -1
        second_path_index = -1
        cycle_detected = False
        if(len(possible_paths) == 0):
            list_of_added_edges.append([smallest_weighted_edge[0], smallest_weighted_edge[1]])
        else:
            for index, path in enumerate(possible_paths):
                if ((smallest_weighted_edge[0] in path) and (smallest_weighted_edge[1] in path)):
                    ##A cycle has been created, so we dont add this node to list_of_added_edges
                    cycle_detected = True
                else:
                    if (smallest_weighted_edge[0] in path):
                        first_path_index = index
                    if (smallest_weighted_edge[1] in path):
                        second_path_index = index
            if (not cycle_detected): 
                list_of_added_edges.append([smallest_weighted_edge[0], smallest_weighted_edge[1]])
                    
        if first_path_index != -1 and second_path_index !=-1:
            # Merge of the 2 lists of possible_path
            possible_paths[first_path_index] = possible_paths[first_path_index] + possible_paths[second_path_index]
            possible_paths.pop(second_path_index)
        elif first_path_index != -1:
            # Add the node to the list of possible_path
            possible_paths[first_path_index].append(smallest_weighted_edge[1])
        elif second_path_index !=-1:
            # Add the node to the list of possible_path
            possible_paths[second_path_index].append(smallest_weighted_edge[0])
        elif not cycle_detected: 
            # None of the 2 nodes of the edge belong to a possible_path so we create a new possible_path
            possible_paths.append([smallest_weighted_edge[0], smallest_weighted_edge[1]])
    return list_of_added_edges
           
          