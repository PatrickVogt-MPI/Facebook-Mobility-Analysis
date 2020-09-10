import graph_construction as gc
import settings
from networkx import DiGraph
from pathlib import Path
from typing import List

# what type hint **kwargs?
def search_edges(graph: DiGraph, **kwargs):
    '''
    Searches edges of a graph for property values and returns list of resulting edge identifier

    Args:
        graph:    Graph object
        **kwargs: edge property key, search value pairs

    Returns:
        edges: list of edge identifier (= node identifier tuples) that fulfill the search criteria
    '''
    edges = []
    for node1, node2, data in graph.edges.data():
        if (all(data[key] == value for key, value in kwargs.items())):
            edges.append((node1, node2))
    return edges
    
def search_nodes(graph: DiGraph, **kwargs):
    '''
    Searches nodes of a graph for property values and returns list of resulting node identifier

    Args:
        graph:    Graph object
        **kwargs: node property key, search value pairs

    Returns:
        nodes: list of node identifier (= natural number) that fulfill the search criteria
    '''
    nodes = []
    for node, data in graph.nodes.data():
        if (all(data[key] == value for key, value in kwargs.items())):
            nodes.append(node)           
    return nodes
    
def search_graphs(graphs: List[DiGraph], **kwargs):
    '''
    Searches a graph for property values and returns list of resulting graphs

    Args:
        graphs:   list of Graph objects
        **kwargs: graph property key, search value pairs

    Returns:
        _graphs: list of graphs that fulfill the search criteria
    '''
    _graphs = []
    for graph in graphs:
        if (all(graph.graph[key] == value for key, value in kwargs.items())):
            _graphs.append(graph)
    return _graphs
    
def adjacency_matrix (graph):
    pass

if __name__ == '__main__':
    graphs = gc.create_movement_graphs_from_csv(settings.settings['data_dir'], '', use_global_nodes = False)
    
    for graph in graphs:
        print(f'Nodes: {len(graph.nodes)}')
        print(f'Edges: {len(graph.edges)}')
        print()