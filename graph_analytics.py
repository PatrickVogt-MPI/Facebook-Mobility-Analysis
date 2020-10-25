import graph_construction as gc
import networkx as nx
import settings
import plotting
import sys
import csv
import numpy as np
from networkx import DiGraph
from pathlib import Path
from timeit import default_timer as timer
from networkx.classes.reportviews import NodeView
from itertools import islice

import testgraph

def search_edges(graph: DiGraph, **kwargs) -> list:
    '''
    Searches edges of a graph for property values and returns list of resulting edges

    Args:
        graph:    DiGraph object
        **kwargs: edge property=search value

    Returns:
        edges: list of edges that fulfill the search criteria
    '''
    edges = []
    for id1, id2, data in graph.edges.data():
        if (all(data[key] == value for key, value in kwargs.items())):
            edges.append((id1, id2, data))
    return edges
    
def search_nodes(graph: DiGraph, **kwargs) -> list:
    '''
    Searches nodes of a graph for property values and returns list of resulting nodes

    Args:
        graph:    DiGraph object
        **kwargs: property key=search value

    Returns:
        nodes: list of nodes
    '''
    nodes = []
    for id, data in graph.nodes.data():
        if (all(data[key] == value for key, value in kwargs.items())):
            nodes.append((id, data))           
    return nodes
    
def search_graphs(graphs: list, **kwargs) -> list:
    '''
    Searches a graph for property values and returns list of resulting graphs

    Args:
        graphs:   list of DiGraph objects
        **kwargs: graph property key, search value pairs

    Returns:
        _graphs: list of graphs that fulfill the search criteria
    '''
    _graphs = []
    for graph in graphs:
        if (all(graph.graph[key] == value for key, value in kwargs.items())):
            _graphs.append(graph)
    return _graphs

def write_map_maker_coordinates_to_csv(path: str, nodes: NodeView):
    '''
    Translates nodes in https://maps.co/ readable coordinates

    Args:
        path:  path to file containing the coordinates
        nodes: Networkx class NodeView of node ids
    '''
    coordinates = len(nodes)
    layers = coordinates // 999 if coordinates % 999 == 0 else coordinates // 999 + 1
    for layer in range(1, layers + 1):
        with open(Path(path + str(layer) + '.csv'), 'w') as file:
            for (lat, lon) in list(nodes)[999*(layer-1):999*layer]:
                file.write(f'{lat},{lon}\n')
                    
def print_graph_info(graph: DiGraph):
    '''
    Prints path to file, number of nodes and number of edges of graph.

    Args:
        graph: DiGraph object
    '''
    seperator_length = max(len(f'Graph data file: {graph.graph["file"]}'), len(f'Number of nodes: {len(graph.nodes)}'), len(f'Number of edges: {len(graph.edges)}'))   
    print()
    print(f'Graph data file: {graph.graph["file"]}')
    print('-'*seperator_length)
    print(f'Number of nodes: {len(graph)}')
    print(f'Number of edges: {len(graph.edges)}')
    print()

def print_connection_info(graph: DiGraph):
    '''
    Lists number of nodes of every degree in the graph and their relative occurance frequency

    Args:
        graph: DiGraph object
    '''
    degree = [graph.degree[id] for id in graph.nodes]
    for i in range(1, max(degree)+1):
        print(f'Number of nodes of degree {i}: {degree.count(i)} | {"{:.2%}".format(degree.count(i)/len(graph.nodes))}')
    print()

def all_simple_paths(graph: DiGraph, source_id, target_id, cutoff=None) -> list:
    '''
    Generates a list of all paths without repeated nodes between two specified nodes.
    A path is a list of edge identifiers.

    Args:
        graph:     DiGraph object
        source_id: node id of source node
        source_id: node id of target node
        cutoff:    depth of maximal path length

    Returns:
        set of all paths from source to target whose depth do not exceed the cutoff value
    '''
    return [path for path in nx.all_simple_paths(graph, source_id, target_id, cutoff=cutoff)]
    
def sorted_weakly_connected_components(graph: DiGraph) -> list:
    '''
    Prints path to file, number of nodes and number of edges of graph.

    Args:
        graph: DiGraph object
        
    Returns:
        Descending, sorted list of sets of weakly connected components based on number of nodes.
    '''
    return [component for component in sorted(nx.weakly_connected_components(graph), key=len, reverse=True)]

def calculate_state_vector (matrix, vector, steps = 1):
    if (steps == 0):
        return vector
    for i in range(steps-1):
        matrix = matrix @ matrix
    
    print(matrix)
    return (matrix @ vector)

def standard_deviation_edges_per_node (graph):
    return np.std([i[1] for i in graph.degree])
    
def arithmetic_mean_edges_per_node(graph):
    return len(graph.edges)/len(graph.nodes)

def k_shortest_paths(graph, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(graph, source, target, weight=weight), k))
    
def k_random_simple_paths (graph, source, tarket, k):
    pass
    
def has_path(G, source, target):
    """Return True if G has a path from source to target, False otherwise.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : node
       Ending node for path
    """
    try:
        sp = nx.shortest_path(G,source, target)
    except nx.NetworkXNoPath:
        return False
    return True
    
if __name__ == '__main__':
    sys.stdout = open('output.txt', 'w')
    #graphs = gc.create_movement_graphs_from_csv(settings.settings['data_dir'], key = '2020-04-29 0000', allow_loops = True, negate_weight = False, remove_isolates = False, display_runtime=True)
    #for graph in graphs:
    #    print_graph_info(graph)
    
    G = nx.from_dict_of_dicts(testgraph.test)
    print(f'Nodes: {G.nodes}')
    print(f'Edges: {G.edges.data()}')
    
        
    '''
        lst = [node for node in sorted_weakly_connected_components(graph)[0]]
        H = nx.subgraph(graph, lst)
        print()
        print_graph_info(H)
    '''
    '''
        start = timer()
        for path in k_shortest_paths(H, (-23.412846680236594, -46.746826171875), (-23.855697620153656, -46.70288085937501), 30000):
            print(path)
            print()
        end = timer()
        print(f'Runtime Shortest Paths: {end - start} seconds')
    '''
            