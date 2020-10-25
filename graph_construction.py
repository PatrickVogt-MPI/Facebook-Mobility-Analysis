# Definitions:
# Nodes are defined as tuples: node = (id: (lat: float, lon: float)), property: dict)
#   id is the unique (lat, lon) tuple of the node and serves as identifier
#   property contains the node attributes derived from the .csv data set
# Edges are defined as 3-tuples: edge = (id1: (lat: float, lon: float), id2: (lat: float, lon: float), property: dict)
#   id1 is the id of the start node
#   id2 is the id of the end node
#   property contains the edge attributes derived from the .csv data set

import csv
import networkx as nx
import numpy as np
import re
from pathlib import Path
from timeit import default_timer as timer

def create_movement_graphs_from_csv(path: Path, key: str = None, allow_loops = True, negate_weight = False, remove_isolates = False, display_runtime: bool = False) -> list:
    '''
    Creates a list of graph data structures from all .csv files found in directory <path>

    Args:
        path:   Path pointing to the data directory of .csv files
        key:    Search key for file names
        
    Returns:
        graphs: List of graph data structures created from each .csv file at the <path> directory. Returns 'None' instead, if empty
    '''
    
    start = timer()
    
    pattern = '*' + key + '*.csv' if key else '*.csv'
    csv_paths = [csv_path for csv_path in Path(path).glob(pattern)]
    
    graphs = []
    
    for path in csv_paths:  
        with open(path, encoding='utf8') as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            
            edges, nodes = [], []
            n_total      = 0
            
            for row in dict_reader:
                coordinates = re.findall(r"[-]?[0-9]*\.[0-9]*", row['geometry'])
                
                graph_properties = {
                    'date_time': row['date_time'],
                    'level':     row['level'],
                    'tile_size': int(row['tile_size']),
                    'file':      path.name
                }
                start_node_id = (float(coordinates[1]), float(coordinates[0])) # (lat, lon)
                start_node_properties = {
                    'polygon_lat':  float(row['start_lat']),
                    'polygon_lon':  float(row['start_lon']),
                    'polygon_id':   int(row['start_polygon_id']),
                    'polygon_name': row['start_polygon_name'],
                    'country':      row['country']
                    #'quadkey':      int(row['start_quadkey'])
                }
                end_node_id = (float(coordinates[3]), float(coordinates[2]))   # (lat, lon)
                end_node_properties = {
                    'polygon_lat':  float(row['end_lat']),
                    'polygon_lon':  float(row['end_lon']),
                    'polygon_id':   int(row['end_polygon_id']),
                    'polygon_name': row['end_polygon_name'],
                    'country':      row['country']
                    #'quadkey':      int(row['end_quadkey'])
                }
                edge_properties = {
                    'weight':         None,
                    'n_crisis':       int(row['n_crisis']),
                    'n_baseline':     float(row['n_baseline']),
                    'length_km':      float(row['length_km']),
                    'n_difference':   float(row['n_difference']),
                    'z_score':        float(row['z_score']),
                    'percent_change': float(row['percent_change']),
                }
                
                n_total += edge_properties['n_crisis']
                
                start_node = (start_node_id, start_node_properties)
                end_node = (end_node_id, end_node_properties)
                
                nodes.extend([start_node, end_node])
                edges.append((start_node_id, end_node_id, edge_properties))
                       
            graph = nx.DiGraph(**graph_properties)
            graph.add_nodes_from(nodes)
            graph.add_edges_from(edges)
            
            # Add weight
            adj_matrix = nx.to_dict_of_dicts(graph)            
            for origin in graph.nodes:
                sum = 0
                for target in adj_matrix[origin]:
                    sum += graph[origin][target]['n_crisis']
                for target in adj_matrix[origin]:
                    weight = graph[origin][target]['n_crisis']/sum
                    #graph[origin][target]['weight'] = -weight if negate_weight else weight
                    graph[origin][target]['weight'] = 1
                    
            if(not allow_loops):
                graph.remove_edges_from(nx.selfloop_edges(graph))
            if(remove_isolates):
                graph.remove_nodes_from(list(nx.isolates(graph)))
         
            graphs.append(graph)
    
    end = timer()
    
    if (display_runtime): print(f'Runtime Graph Creation: {end - start} seconds')
    
    return graphs if graphs else None
    
def save_movement_graph_to_file():
    pass
        
def read_movement_graph_from_file():
    pass