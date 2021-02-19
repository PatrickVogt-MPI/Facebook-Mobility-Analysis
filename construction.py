import analytics
import csv
import re
import settings
import utility
import networkx  as     nx
import pandas    as     pd
from   functools import reduce
from   pathlib   import Path
from   networkx  import Graph
from   networkx  import DiGraph

###########################################################################
### Disclaimer - All RKI related functions work perfectly,              ###
### but RKI data set is inconsistent (missing/added columns over time). ###
### Consistency starts around 2020-06-01+.                              ###
###########################################################################

def movement_graph(path: str) -> DiGraph:
    '''
    Creates a movement graph from a .csv file at <path>

    Args:
        path: path pointing to the .csv file
        
    Returns:
        graph: DiGraph data structure
    '''    
    
    with open(Path(path), encoding='utf8') as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=',')  
        
        edges, nodes = [], []
        
        for row in dict_reader:
            try:
                date_time          = pd.to_datetime(row['date_time'], format='%Y-%m-%d %H%M')
                tile_size          = int(row['tile_size'])
                file               = path.name
                country            = row['country']
                start_lat          = float(row['start_lat'])
                start_lon          = float(row['start_lon'])
                start_polygon_id   = int(row['start_polygon_id'])
                start_polygon_name = row['start_polygon_name']
                start_quadkey      = row['start_quadkey']
                end_lat            = float(row['end_lat'])
                end_lon            = float(row['end_lon'])
                end_polygon_id     = int(row['end_polygon_id'])
                end_polygon_name   = row['end_polygon_name']
                end_quadkey        = row['end_quadkey']
                n_crisis           = int(row['n_crisis'])
                length_km          = float(row['length_km'])
            except:
                print(f'[ERROR] Unable to read data.')
                return None
                
            graph_properties = {
                'date_time': date_time,
                'tile_size': tile_size,
                'mov_file':  file,
            }
            start_node_properties = {
                'lat':          start_lat,
                'lon':          start_lon,
                'polygon_id':   start_polygon_id,
                'polygon_name': start_polygon_name,
                'country':      country,
            }
            end_node_properties   = {
                'lat':          end_lat,
                'lon':          end_lon,
                'polygon_id':   end_polygon_id,
                'polygon_name': end_polygon_name,
                'country':      country,
            }
            edge_properties  = {
                'n_crisis':  n_crisis,
                'length_km': length_km,
            }
                
            start_node = (start_quadkey, start_node_properties)
            end_node   = (end_quadkey, end_node_properties)    
            nodes.extend([start_node, end_node])
            edges.append((start_quadkey, end_quadkey, edge_properties))
                       
    graph = nx.DiGraph(**graph_properties)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    
    return graph

def administrative_movement_graph(path: str) -> DiGraph:
    '''
    Creates a movement graph (administrative level) from a .csv file at <path>

    Args:
        path: path pointing to the .csv file
        
    Returns:
        graph: DiGraph data structure
    '''    
    with open(Path(path), encoding='utf8') as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=',')  
        
        edges, nodes = [], []
        
        for row in dict_reader:
            try:
                date_time          = pd.to_datetime(row['date_time'], format='%Y-%m-%d %H%M')
                tile_size          = int(row['tile_size'])
                file               = path.name
                country            = row['country']
                start_lat          = float(row['start_lat'])
                start_lon          = float(row['start_lon'])
                start_polygon_id   = int(row['start_polygon_id'])
                start_polygon_name = row['start_polygon_name']
                end_lat            = float(row['end_lat'])
                end_lon            = float(row['end_lon'])
                end_polygon_id     = int(row['end_polygon_id'])
                end_polygon_name   = row['end_polygon_name']
                n_crisis           = int(row['n_crisis'])
                length_km          = float(row['length_km'])
            except:
                print(f'[ERROR] Unable to read data.')
                return None
                
            graph_properties = {
                'date_time':      date_time,
                'tile_size':      tile_size,
                'mov_admin_file': file,
            }
            start_node_properties = {
                'polygon_id':   start_polygon_id,
                'polygon_name': start_polygon_name,
                'country':      country,
            }
            end_node_properties   = {
                'polygon_id':   end_polygon_id,
                'polygon_name': end_polygon_name,
                'country':      country,
            }
            edge_properties  = {
                'n_crisis':  n_crisis,
                'length_km': length_km,
            }
            start_node_id = (start_lat, start_lon)
            end_node_id = (end_lat, end_lon)
            start_node = (start_node_id, start_node_properties)
            end_node   = (end_node_id, end_node_properties)
            
            nodes.extend([start_node, end_node])
            edges.append((start_node_id, end_node_id, edge_properties))
                       
    graph = nx.DiGraph(**graph_properties)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    
    return graph
   
def population_graph(path: str) -> Graph:
    '''
    Creates a population graph from a .csv file at <path>

    Args:
        path: path pointing to the .csv file
        
    Returns:
        graph: Graph data structure
    ''' 
    nodes = []

    with open(Path(path), encoding='utf8') as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=',')
        for row in dict_reader:
            try:
                date_time  = pd.to_datetime(row['date_time'], format='%Y-%m-%d %H%M')
                quadkey    = row['quadkey']
                lat        = float(row['lat'])
                lon        = float(row['lon'])
                country    = row['country']
                population = float(row['n_crisis'])
            except:
                continue
            graph_properties = {
                'date_time': date_time,
                'tile_size': len(str(quadkey)),
                'pop_file':  Path(path).name,
            }
            node_properties = {
                'lat':        lat,
                'lon':        lon,
                'country':    country,
                'population': population,
            }
            node = (quadkey, node_properties)
            nodes.append(node)
        
    graph = nx.Graph(**graph_properties)
    graph.add_nodes_from(nodes)
        
    return graph

def administrative_population_graph(path: str) -> Graph:
    '''
    Creates a population graph (administrative level) from a .csv file at <path>

    Args:
        path: path pointing to the .csv file
        
    Returns:
        graph: Graph data structure
    ''' 
    nodes = []
    with open(Path(path), encoding='utf8') as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=',')
        for row in dict_reader:
            try:
                date_time    = pd.to_datetime(row['date_time'], format='%Y-%m-%d %H%M')
                lat          = float(row['lat'])
                lon          = float(row['lon'])
                country      = row['country']
                polygon_name = row['polygon_name']
                population   = float(row['n_crisis'])
            except:
                continue
            
            graph_properties = {
                'date_time':       date_time,
                'pop_admin_file': Path(path).name,
            }
            node_properties = {
                'country':      country,
                'polygon_name': polygon_name,
                'population':   population,
            }
            node_id = (lat, lon)
            node    = (node_id, node_properties)
            nodes.append(node)
        
    graph = nx.Graph(**graph_properties)
    graph.add_nodes_from(nodes)
        
    return graph

# If time: Add name parameter for more convenient use, add more file formats     
def save_graph(graph: Graph, path: str, format: str = 'GraphML'):
    '''
    Stores a graph data structure in files of type <format> at <path>.
    Name ...\<name>.graphml must be included in path.

    Args:
        graph:  Graph object
        path:   path pointing to storage directory
        format: storage file format
    '''
    graph.graph['date_time'] = str(graph.graph['date_time'])
    if('GraphML'):
        try:
            nx.write_graphml(graph, Path(path))
        except:
            print(f'[ERROR] Unable to write graph to file at location {path}.')
        return
    print('[ERROR] Unknown data format.')  
    
def read_graph(path: str, format: str = 'GraphML') -> Graph:
    '''
    Reads a graph data structure from file of type <format> at <path>.

    Args:
        path:   path pointing to graph data file
        format: graph data file format
        
    Returns:
        graph:  graph data structure
    '''
    if('GraphML'):
        try:
            graph = nx.read_graphml(Path(path))
            graph.graph['date_time'] = pd.Timestamp(graph.graph['date_time'])
            return graph
        except:
            print(f'[ERROR] Unable to read file at location {path}.')
            return
    print('[ERROR] Unknown data format.')

# If time: border tiles? Add lat lon and country?    
def space_aggregate_population_graph(graph: Graph, delta: int = 1) -> Graph:
    '''
    Aggregates an existing population graph to arbitrarily lower tile resolution.

    Args:
        graph: (population) Graph data structrue
        delta: change of tile level
        
    Returns:
        graph: Graph data structure
    '''  
    if(delta < 1 or graph.graph['tile_size'] == 1): return graph
   
    quadkeys = sorted(list(graph.nodes))
    agg_nodes = []
    
    while(quadkeys):
        agg_quadkey = quadkeys[0][:-1]
        
        agg_population = 0
        
        for i in range(0, 4):
            quadkey = agg_quadkey + str(i)
            if quadkey in quadkeys:
                properties = graph.nodes[quadkey]
                agg_population += properties['population']
                quadkeys.remove(quadkey)
        
        agg_properties = {'population': agg_population}
        
        agg_node = (agg_quadkey, agg_properties)
        agg_nodes.append(agg_node)
    
    agg_graph_properties = {
        'date_time': graph.graph['date_time'],
        'tile_size': graph.graph['tile_size'] - 1,
        'pop_file':  graph.graph['pop_file'],
    }
    
    agg_graph = nx.Graph(**agg_graph_properties)
    agg_graph.add_nodes_from(agg_nodes)
    
    return space_aggregate_population_graph(agg_graph, delta-1)

# If time: Add parameter for slicing/timeframe
def time_aggregate_movement_graph(graphs: list) -> Graph:
    '''
    Aggregates a set of (administrative) movement graphs over an arbitrary timeframe.

    Args:
        graphs:  List of DiGraph objects
        
    Returns:
        merged_graph: DiGraph object 
    '''
    if(not graphs):
        print('[ERROR] Empty list - no graphs to aggregate.')
        
    agg_graph = nx.DiGraph()
    
    for graph in graphs:
        for id, data in graph.nodes.data():
            if (id not in agg_graph):
                agg_graph.add_nodes_from([(id, data)])
        for id1, id2, data in graph.edges.data():
            if (agg_graph.has_edge(id1, id2)):
                agg_graph[id1][id2]['n_crisis']   += data['n_crisis']
                agg_graph[id1][id2]['length_km']  += data['length_km']
            else:
                edge_properties = {key: data[key] for key in ('n_crisis', 'length_km')}
                agg_graph.add_edges_from([(id1, id2, edge_properties)])
                
    return agg_graph
    
def time_aggregate_admin_population_graph(graphs: List[Graph], slice: int = 3) -> Graph:
    '''
    Aggregates a set of (administrative) population graphs over an arbitrary timeframe.

    Args:
        graphs: List of Graph objects
        slice:  Splits list in consecutive fractions of <slice> items (default: 3 8-hour-timeframes = 1 day)
        
    Returns:
        merged_graph: Graph object 
    '''
    if(not graphs):
        print('[ERROR] Empty list - no graphs to aggregate.')
        
    agg_graphs = []
    
    graph_slices = [graphs[i*slice:i*slice + slice] for i in range(len(graphs)//slice)]
    for slice in graph_slices:
        agg_graph = nx.DiGraph(date_time = [], pop_admin_file = [])
        
        for graph in slice:
            agg_graph.graph['date_time'].append(graph.graph['date_time'])
            agg_graph.graph['pop_admin_file'].append(graph.graph['pop_admin_file'])        
            
            for id, data in graph.nodes.data():
                if (id not in agg_graph):
                    agg_graph.add_nodes_from([(id, data)])
                else:
                    agg_graph.nodes[id]['population'] += data['population']     

        agg_graphs.append(agg_graph)
        
    return agg_graphs    
   
def merge_population_with_movement_graph(pop_graph, mov_graph) -> DiGraph:
    '''
    Merges (nodes, edges, graph properties of) population graph with movement graph of identical tile resolution.

    Args:
        pop_graph:  (population) Graph object
        mov_graph:  (movement)   DiGraph object
        
    Returns:
        merged_graph: DiGraph object 
    '''
    pop_date_time = pop_graph.graph['date_time']
    pop_tile_size = pop_graph.graph['tile_size']
    mov_date_time = mov_graph.graph['date_time']
    mov_tile_size = mov_graph.graph['tile_size']
    
    if(pop_date_time != mov_date_time):
        print('[ERROR] Unable to merge graphs with different date_time.')
        return None
    if(pop_tile_size < mov_tile_size):
        print('[ERROR] Unable to merge movement graph with lower resolution population graph.')
        return None
        
    pop_graph = space_aggregate_population_graph(pop_graph, pop_tile_size - mov_tile_size)
    merged_graph = nx.compose(mov_graph, pop_graph)
    return merged_graph            
  
def cumulated_infected(start_date: str = '2020-06-01', end_date: str = '', **kwargs) -> int:
    '''
    Calculates the number of infected people within <start_date> and <end_date> (both dates inclusive).
    If end_date is empty, system time will be selcted.
    
    Args:
        start_date: date-string of format 'DD.MM.YY'
        end_date:   date-string of format 'DD.MM.YY'
        kwargs:     filter for values of columns in .csv file, e.g. Bundesland='Bayern' or Altersgruppe='A15-A34'
        
    Returns:
        count: number of infected people 
    '''
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    if(end_date):
        end = pd.to_datetime(end_date, format='%Y-%m-%d')
    else:
        end = pd.Timestamp.now().normalize()
    
    path = f'{settings.paths["RKI"]}\\{end.month_name()}{str(end.year)}\\RKI_COVID19_{end.date()}.csv'
    col  = ['AnzahlFall', 'NeuerFall', 'Meldedatum'] + list(kwargs)
    
    df = pd.read_csv(path, usecols=col, parse_dates=['Meldedatum'])
    
    mask  = (df['NeuerFall'] >= 0) & (df['Meldedatum'] >= start) & (df['Meldedatum'] <= end)
    for key, value in kwargs.items():
        mask &= (df[key] == value)
    
    count = df.loc[mask].sum()['AnzahlFall']
    return count
    
def cumulated_recovered(start_date: str = '2020-06-01', end_date: str = '', **kwargs) -> int:
    '''
    Calculates the number of recovered people within <start_date> and <end_date> (both dates inclusive).
    If end_date is empty, system time will be selcted.

    Args:
        start_date: date-string of format 'YYYY-MM-DD'
        end_date:   date-string of format 'YYYY-MM-DD'
        kwargs:     filter for values of columns in .csv file, e.g. Bundesland='Bayern' or Altersgruppe='A15-A34'
        
    Returns:
        count: number of recovered people 
    '''
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    if(end_date):
        end   = pd.to_datetime(end_date, format='%Y-%m-%d')
    else:
        end = pd.Timestamp.now().normalize()
        
    path  = f'{settings.paths["RKI"]}\\{end.month_name()}{str(end.year)}\\RKI_COVID19_{end.date()}.csv'
    col   = ['AnzahlGenesen', 'NeuGenesen', 'Meldedatum'] + list(kwargs)
    df    = pd.read_csv(path, usecols=col, parse_dates=['Meldedatum'])
    
    mask  = (df['NeuGenesen'] >= 0) & (df['Meldedatum'] >= start) & (df['Meldedatum'] <= end)
    for key, value in kwargs.items():
        mask &= (df[key] == value)
    
    count = df.loc[mask].sum()['AnzahlGenesen']
    return count

def cumulated_dead(start_date: str = '2020-06-01', end_date: str = '', **kwargs) -> int:
    '''
    Calculates the number of deaths within <start_date> and <end_date> (both dates inclusive).
    If end_date is empty, system time will be selcted.

    Args:
        start_date: date-string of format 'YYYY-MM-DD'
        end_date:   date-string of format 'YYYY-MM-DD'
        kwargs:     filter for values of columns in .csv file, e.g. Bundesland='Bayern' or Altersgruppe='A15-A34'
        
    Returns:
        count: number of deaths
    '''
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    if(end_date):
        end   = pd.to_datetime(end_date, format='%Y-%m-%d')
    else:
        end = pd.Timestamp.now().normalize()
    
    path  = f'{settings.paths["RKI"]}\\{end.month_name()}{str(end.year)}\\RKI_COVID19_{end.date()}.csv'
    col   = ['AnzahlTodesfall', 'NeuerTodesfall', 'Meldedatum'] + list(kwargs)
    df    = pd.read_csv(path, usecols=col, parse_dates=['Meldedatum'])
    
    mask  = (df['NeuerTodesfall'] >= 0) & (df['Meldedatum'] >= start) & (df['Meldedatum'] <= end)
    for key, value in kwargs.items(): 
        mask &= (df[key] == value)
        
    count = df.loc[mask].sum()['AnzahlTodesfall']
    return count
    
def currently_infected(date: str = '', **kwargs) -> int:
    '''
    Calculates the number of infected people until <date> (date inclusive).

    Args:
        date:   date-string of format 'YYYY-MM-DD'
        kwargs: filter for values of columns in .csv file, e.g. Bundesland='Bayern' or Altersgruppe='A15-A34'
        
    Returns:
        current: number of infected people
    
    Secondary source of past RKI-csv files:
    https://github.com/CharlesStr/CSV-Dateien-mit-Covid-19-Infektionen-
    
    RKI-dashboard:
    https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4
    '''
    infected  = cumulated_infected(end_date = date, **kwargs)
    recovered = cumulated_recovered(end_date = date, **kwargs)
    dead      = cumulated_dead(end_date = date, **kwargs)
    current   = infected - recovered - dead
    return current