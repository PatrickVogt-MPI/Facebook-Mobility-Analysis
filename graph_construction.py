# Why is 'LINESTRING' different from start_lat, start_lon / end_lon, end_lat? Intrinsic consistency of start/end lat/lon though
# What is the purpose of 'is_statistically_significant'?
# Some maps are missing Quadkeys? --> Check for properties

import csv
import networkx as nx
from pathlib import Path
    
def create_movement_graph(*paths):

    def add_unique_node(pivot):
        for node in nodes:
            if(node[1]['lat'] == pivot['lat'] and node[1]['lon'] == pivot['lon']): return node[0]
        nodes.append((len(nodes)+1, pivot))
        return nodes[-1][0]
    
    graphs = []
    
    for path in paths:
    
        nodes, edges = [], []
        
        with open(str(path), newline='') as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            
            for row in dict_reader:
                graph_properties = {
                    'date_time': row['date_time'],
                    'level':     row['level'],
                    'tile_size': int(row['tile_size'])
                }
                start_node_properties = {
                    'lat':          float(row['start_lat']),
                    'lon':          float(row['start_lon']),
                    'country':      row['country'],
                    'polygon_id':   int(row['start_polygon_id']),
                    'polygon_name': row['start_polygon_name'],
                    #'quadkey':      int(row['start_quadkey'])
                }
                end_node_properties = {
                    'lat':          float(row['end_lat']),
                    'lon':          float(row['end_lon']),
                    'country':      row['country'],
                    'polygon_id':   int(row['end_polygon_id']),
                    'polygon_name': row['end_polygon_name'],
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
                tile_size = graph_properties['tile_size']
            )
            DG.add_nodes_from(nodes)
            DG.add_edges_from(edges)
            graphs.append(DG)   
        
    return graphs    

def create_movement_graphs_from_csv(path):
    data_dir = [_ for _ in Path(path).glob('*.csv')]
    return create_movement_graph(*data_dir)
    
def save_movement_graph():
    pass
        
def read_movement_graph_from_file():
    pass