import graph_construction as gc
import settings
from networkx import DiGraph
from pathlib import Path

def search_edges(graph: DiGraph, **kwargs) -> list:
    '''
    Searches edges of a graph for property values and returns list of resulting edges

    Args:
        graph:    Graph object
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
        graph:    Graph object
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

def write_map_maker_coordinates_to_csv(path: str, nodes: list):
    '''
    Translates nodes in https://maps.co/ readable coordinates

    Args:
        path:  path to file containing the coordinates
        nodes: list of node-tuples of the form (id: int, property: dict)
    '''
    coordinates = len(nodes)
    layers = coordinates // 999 if coordinates % 999 == 0 else coordinates // 999 + 1
    for layer in range(1, layers + 1):
        with open(Path(path + str(layer) + '.csv'), 'w') as file:
            for id, data in nodes[999*(layer-1):999*layer]:
                file.write(f'{data["lon"]},{data["lat"]}\n')

def print_graph_info(graphs: list):
    for graph in graphs:
        seperator_length = max(len(f'Graph: {graph.graph["file"]}'), len(f'Nodes: {len(graph.nodes)}'), len(f'Edges: {len(graph.edges)}'))
        
        print()
        print(f'Graph: {graph.graph["file"]}')
        print('-'*seperator_length)
        print(f'Nodes: {len(graph.nodes)}')
        print(f'Edges: {len(graph.edges)}')
        print()
            
if __name__ == '__main__':
    graphs = gc.create_movement_graphs_from_csv(settings.settings['data_dir'], 'test', use_global_nodes=True, display_runtime=True)
    print_graph_info(graphs)