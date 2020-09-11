# Definitions:
# Nodes are defined as tuples: node = (id: int, property: dict)
#   id is the unique name of the node
#   property contains the node attributes derived from the .csv data set
# Edges are defined as 3-tuples: edge = (id1: int, id2: int, property: dict)
#   id1 is the unique name of the start node
#   id2 is the unique name of the end node
#   property contains the edge attributes derived from the .csv data set

import csv
import networkx as nx
import re
import sys
from pathlib import Path
from timeit import default_timer as timer

def create_movement_graphs_from_csv(path: Path, key: str = None, use_global_nodes: bool = False, display_runtime: bool = False) -> list:
    '''
    Creates a list of graph data structures from all .csv files found in directory <path>

    Args:
        path:   Path pointing to the data directory of .csv files
        key:    Search key for files
        
    Returns:
        graphs: List of graph data structures created from each .csv file at the <path> directory. Returns 'None' instead, if empty
    '''
    def add_unique_node(t_prop: dict) -> int:
        '''
        Adds node with properties 't_node' to list 'g_nodes' if unique and in any case
        adds it to list 'l_nodes' for graph construction and returns its identifier.
        In this code, t stands for test, g for global and  l for local.

        Args:
            t_node: properties of the test node

        Returns:
            g_id:   identifier of global node
            t_id:   identifier of local node
        '''
        for g_id, g_prop in g_nodes:
            if(g_prop['lat'] == t_prop['lat'] and g_prop['lon'] == t_prop['lon']):
                l_nodes.append((g_id, g_prop))
                return g_id
        t_id = len(g_nodes) + 1
        g_nodes.append((t_id, t_prop))
        l_nodes.append((t_id, t_prop))
        return t_id
    
    start = timer()
    
    # Introduction of global_nodes causes consistent identifier for all nodes among all graphs from different .csv files
    graphs, g_nodes, temp = [], [], []
    
    pattern = '*' + key + '*.csv' if key else '*.csv'
    csv_paths = [csv_path for csv_path in Path(path).glob(pattern)]
    
    for path in csv_paths:  
        with open(path, encoding='utf8') as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            
            edges, l_nodes = [], []
            
            for row in dict_reader:
                coordinates = re.findall(r"[-]?[0-9]*\.[0-9]*", row['geometry'])
                
                graph_properties = {
                    'date_time': row['date_time'],
                    'level':     row['level'],
                    'tile_size': int(row['tile_size'])
                }
                start_node_properties = {
                    'lat':          float(coordinates[0]),
                    'lon':          float(coordinates[1]),
                    'polygon_lat':  float(row['start_lat']),
                    'polygon_lon':  float(row['start_lon']),
                    'polygon_id':   int(row['start_polygon_id']),
                    'polygon_name': row['start_polygon_name'],
                    'country':      row['country']
                    #'quadkey':      int(row['start_quadkey'])
                }
                end_node_properties = {
                    'lat':          float(coordinates[2]),
                    'lon':          float(coordinates[3]),
                    'polygon_lat':  float(row['end_lat']),
                    'polygon_lon':  float(row['end_lon']),
                    'polygon_id':   int(row['end_polygon_id']),
                    'polygon_name': row['end_polygon_name'],
                    'country':      row['country']
                    #'quadkey':      int(row['end_quadkey'])
                }
                edge_properties = {
                    'n_crisis':       int(row['n_crisis']),
                    'n_baseline':     float(row['n_baseline']),
                    'length_km':      float(row['length_km']),
                    'n_difference':   float(row['n_difference']),
                    'z_score':        float(row['z_score']),
                    'percent_change': float(row['percent_change']),
                }
      
                start_node = add_unique_node(start_node_properties)
                end_node = add_unique_node(end_node_properties)
                edges.append((start_node, end_node, edge_properties))
            
            DG = nx.DiGraph(
                date_time = graph_properties['date_time'], 
                level     = graph_properties['level'], 
                tile_size = graph_properties['tile_size'],
                file      = path.name
            )
            
            temp.append((DG, l_nodes, edges))
    
    for (graph, l_nodes, edges) in temp:
        if(use_global_nodes):
            graph.add_nodes_from(g_nodes)
        else:
            graph.add_nodes_from(l_nodes)
        graph.add_edges_from(edges)
        graphs.append(graph)
    
    end = timer()
    if (display_runtime): print(f'Runtime: {end - start} seconds')
    
    return graphs if graphs else None
    
def save_movement_graph_to_file():
    pass
        
def read_movement_graph_from_file():
    pass