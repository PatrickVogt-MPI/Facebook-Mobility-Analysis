# Why is 'LINESTRING' different from start_lat, start_lon / end_lon, end_lat?
'''@AlexPompe: 
the linestring coordinates in the Movement Data sets are the average lat+lon of the starting point
and ending point of all users counted in the vector - not the centroid

one set of start / end coordinates are the centroid of the polygons and the other are the average starting and ending coordinates of all users who are represented in that row
'''
# What is the purpose of 'is_statistically_significant'?
# Some maps are missing Quadkeys? --> Check for properties

'''
To do:
    *only allow valid regular expression for 'key' in  'create_movement_graphs_from_csv'
    *add path to csv to edge property
'''

import csv
import networkx as nx
from pathlib import Path
import re

def create_movement_graphs_from_csv(path: Path, key: str=None) -> list:
    '''
    Creates a list of graph data structures from all .csv files found in directory <path>

    Args:
        path:   Path pointing to the data directory of .csv files
        key:    Search key for files
        
    Returns:
        graphs: List of graph data structures created from each .csv file at the <path> directory. Returns 'None' instead, if empty
    '''

    def add_unique_node(pivot: dict) -> int:
        '''
        Adds node with properties 'pivot' to list 'nodes' if unique and in any case returns its identifier.

        Args:
            pivot:        Node properties

        Returns:
            node[0]:      Identifier, node already exists
            nodes[-1][0]: Identifier, node has been added
        '''
        
        for node in nodes:
            if(node[1]['lat'] == pivot['lat'] and node[1]['lon'] == pivot['lon']): 
                return node[0]
                
        nodes.append((len(nodes)+1, pivot))
        return nodes[-1][0]
    
    graphs = []
    
    pattern = '*' + key + '*.csv' if key else '*.csv'
    csv_paths = [csv_path for csv_path in Path(path).glob(pattern)]
    
    for path in csv_paths:
        # Organizes all data from a .csv file as properties in dicts
        with open(str(path), newline='') as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            
            edges, nodes = [], []
            
            for row in dict_reader:
                coordinates = re.findall(r"[-+]?[0-9]*\.[0-9]*", row['geometry'])
                
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
                
                # Adds 'start_node' and 'end_node' to list 'nodes', if unique
                start_node = add_unique_node(start_node_properties)
                end_node = add_unique_node(end_node_properties)

                # Draws edge between 'start_node' and 'end_node'
                edges.append((start_node, end_node, edge_properties))
            
            # Creates graph structure from 'nodes' and 'edges' and adds it to list 'graphs'
            DG = nx.DiGraph(
                date_time = graph_properties['date_time'], 
                level     = graph_properties['level'], 
                tile_size = graph_properties['tile_size']
            )
            DG.add_nodes_from(nodes)
            DG.add_edges_from(edges)
            
            graphs.append(DG)   
            
    return graphs if graphs else None
    
def save_movement_graph():
    pass
        
def read_movement_graph_from_file():
    pass