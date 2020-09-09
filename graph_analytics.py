import graph_construction as gc
import networkx as nx
from pathlib import Path
import settings

def iterate_over_edges(graph, key=None):
    values = []
    for node1, node2, data in graph.edges.data():
        if(key): 
            values.append(data[key])
        else: 
            values.append(data)
    return values
    
def iterate_over_nodes(graph, key=None):
    values = []
    for node, data in graph.nodes.data():
        if(key): 
            values.append(data[key])
        else: 
            values.append(data)
    return values
    
def iterate_over_graphs(graphs, key=None):
    values = []
    for graph in graphs:
        if(key): 
            values.append(graph.graph[key])
        else: 
            values.append(graph.graph)
    return values

graphs = gc.create_movement_graphs_from_csv(settings.settings['data_dir'])

beirut = graphs[0]
print(iterate_over_edges(beirut, 'n_baseline'))
print()
print(iterate_over_nodes(beirut))
print()
print(iterate_over_graphs(graphs, 'level'))