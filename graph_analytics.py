import graph_construction as gc
import settings
from networkx import DiGraph
from pathlib import Path
from typing import List

# list of tuples?
# search propertys rathe than iterate over properties
def iterate_over_edges(graph: DiGraph, key: str=None):
    '''
    Extracts (specified) properties of all edges in a graph

    Args:
        graph:  Graph object
        key:    Dictionary key of an edge property

    Returns:
        values: List with values of edge property 'key' for all edges in 'graph'. Returns list of property dicts instead, if 'key=None'
    '''
    values = []
    for node1, node2, data in graph.edges.data():
        if(key): 
            values.append(data[key])
        else: 
            values.append(data)
    return values
    
def iterate_over_nodes(graph: DiGraph, key:str=None):
    '''
    Extracts (specified) properties of all nodes in a graph

    Args:
        graph:  Graph object
        key:    Dictionary key of a node property

    Returns:
        values: List with values of node property 'key' for all nodes in 'graph'. Returns list of property dicts instead, if 'key=None'
    '''
    values = []
    for node, data in graph.nodes.data():
        if(key): 
            values.append(data[key])
        else: 
            values.append(data)
    return values
    
def iterate_over_graphs(graphs: List[DiGraph], key: str=None):
    '''
    Extracts (specified) properties of all graphs in a list of graphs

    Args:
        graph:  Graph object
        key:    Dictionary key of a graph property

    Returns:
        values: List with values of graph property 'key' for all graphs in 'graphs'. Returns list of whole property dicts instead, if 'key=None'
    '''
    values = []
    for graph in graphs:
        if(key): 
            values.append(graph.graph[key])
        else: 
            values.append(graph.graph)
    return values
    
def adjacency_matrix (graph):
    pass

if __name__ == '__main__':
    graphs = gc.create_movement_graphs_from_csv(settings.settings['data_dir'])
    
    for graph in graphs:
        print(f'Nodes: {len(graph.nodes)}')
        print(f'Edges: {len(graph.edges)}')
        print()
    
    