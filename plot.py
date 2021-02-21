import analytics
import simplekml
import copy
import construction      as con
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import model    as md
import networkx as nx
import numpy    as np
import pandas   as pd
import seaborn  as sns
import utility  as ut
from networkx   import Graph
from typing     import List
import sys
import matplotlib.dates as mdates

##########################################################################################
### DISCLAIMER                                                                         ###
### Did not have time to write cleaner code because of exams.                          ###
### Went a couple times for a 'quick' solution over the 'clean' solution. Sorry!       ###
##########################################################################################

def tile_kml(graph: Graph, name: str):
    '''
    Generates a KML-file showing the outlines of every tile at geospatial position.
    For quick viewing use https://ivanrublev.me/kml/

    Args:
        graph: Graph object
        path:  Path pointing to storage directory
    '''
    kml = simplekml.Kml()
    for node in graph.nodes:
        p0, p1, p2, p3 = analytics.get_tile_vertices(graph.nodes[node]['lon'], graph.nodes[node]['lat'], graph.graph['tile_size'])
        pol = kml.newpolygon(name=node)
        pol.outerboundaryis = [p0, p1, p3, p2, p0]
        pol.style.polystyle.color = simplekml.Color.red
        pol.style.polystyle.outline = 1
    kml.save(name + '.kml')

def plot_nation_currently_infected(date: str = '2020-06-01', store: bool = False, name: str = 'nation-active-infections-plot.png'):
    '''
    DISCLAIMER: RKI data set inconsistent (columns removed/added over time). Stable since June.
    
    Generates a plot of active infections on national level.
    The data point for each day has been calculated with that days publication
    => (Potentially) Late case arrivals excluded.

    Args:
        date:  first date showing on the x-axis (use always 'YYYY-MM-DD' as format)
        store: discards/saves plot as <name>
        name:  name of stored file
        
    Returns:
        fig:   Resulting graph-figure
    '''
    
    fig = plt.figure()
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    
    ts_scale = list(pd.date_range('2020-06-01', date))
    
    ts_currently_infected = []
    for curr in ts_scale:
        ts_currently_infected.append(con.currently_infected(curr.strftime('%Y-%m-%d')))
        
    df = pd.DataFrame({
            'date':               np.array(ts_scale),
            'currently_infected': np.array(ts_currently_infected),
        })
    
    plt.plot(df['date'], df['currently_infected'], marker='', color=palette(1), alpha=0.9)
    
    minimum, maximum = min(ts_currently_infected), max(ts_currently_infected)
    plt.ylim(minimum*0.95, maximum*1.05)
    plt.title('Active infections', loc='center', fontsize=12, fontweight=0, color=palette(1))
    
    x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
    plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.ylabel('Number of active infections in thousands')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: int(y/1000)))
    
    if(store):       
        fig.savefig(name)
    else:
        plt.show()

    return fig  

def plot_state_currently_infected(date: str = '2020-06-01', store: bool = False, name: str = 'state-active-infections-plot.png'):
    '''
    DISCLAIMER: RKI data set inconsistent (columns removed/added over time). Stable since June.
    
    Generates a plot of active infections on state level.
    The data point for each day has been calculated with that days publication.
    => (Potentially) Late case arrivals excluded.

    Args:
        date:  first date showing on the x-axis (use always 'YYYY-MM-DD' as format)
        store: discards/saves plot as <name>
        name:  name of stored file
        
    Returns:
        fig:   Resulting graph-figure
    '''
    fig = plt.figure()
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    
    ts_scale = list(pd.date_range('2020-06-01', date))
    
    states = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
              'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
              'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
              'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
    
    num = 0
    for state in states:
        num += 1
        
        ts_currently_infected = []
        for curr in ts_scale:
            ts_currently_infected.append(con.currently_infected(curr.strftime('%Y-%m-%d'), Bundesland=state))       
        
        minimum, maximum = min(ts_currently_infected), max(ts_currently_infected)
        
        df = pd.DataFrame({
            'date':               np.array(ts_scale),
            'currently_infected': np.array(ts_currently_infected),
        })
        
        plt.subplot(4,4, num)
        plt.plot(df['date'], df['currently_infected'], marker='', color=palette(1), alpha=0.9)
        plt.ylim(minimum*0.95, maximum*1.05)        
        plt.title(state, loc='center', fontsize=12, fontweight=0, color=palette(1))
        
        if num in range(1, 16, 4):
            plt.ylabel('Facebook population in thousands')
        if num in range(1, 13) :
            plt.tick_params(labelbottom=False)
            
        x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
        plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.ylabel('Number of active infections in thousands')
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: int(y/1000)))
    
        break
    
    if(store):       
        fig.savefig(name, dpi=320)
    else:
        plt.show()

    return fig  
    
def plot_SIR(ts_susceptible: List[float], ts_infected: List[float], ts_recovered: List[float], ts_scale: List[float], title: str, store: bool = False, name: str = 'SIR-plot.png'):
    '''
    Creates and saves a plot of susceptible, infected and recovered people over time of an SIR-model.

    Args:
        ts_susceptible: time series of number of susceptible people
        ts_infected:    time series of number of infected people
        ts_recovered:   time series of number of recovered people
        
    Returns:
        plot: 'plot object' of SIR dynamics (need to look up type)
    '''
    
    data_preproc = pd.DataFrame({
        time_unit:     np.array(ts_scale),
        'susceptible': np.array(ts_susceptible),
        'infected':    np.array(ts_infected),
        'recovered':   np.array(ts_recovered),
    })
    
    sns.set_theme()
    sns.set(style='darkgrid')
    plot = sns.lineplot(x=time_unit, y='value', hue='variable', data=pd.melt(data_preproc, [time_unit]))
    
    if(store):
        fig = plot.get_figure()
        fig.savefig(name)
    
    return plot

# Change position based slicing to date slicing, use None value for missing data points, add timeframe slicing   
def plot_state_population(graphs: List[Graph], start_date: str = '2020-03-25', store: bool = False, name: str = 'state-population-plot.png'):
    '''
    DISCLAIMER: Two missing dates in Facebook data set. Lack of time => went for the 'quick' solution. Will make function more error robust.
    
    Generates plot of Facebook population for each state over time.

    Args:
        graphs:     list of administrative population graphs
        start_date: date-time string of first graph showing on x-axis
        store:      discards/saves plot as <name>
        name:       name of stored file
        
    Returns:
        fig: resulting graph-figure
    '''
    fig = plt.figure(figsize=(32, 18))
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    
    curr_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    ts_scale  = []
    # cheating
    for i in range(len(graphs)//3 + 1):
        ts_scale.append(curr_date)
        curr_date += pd.Timedelta(days=1)
    
    num = 0
    for id in graphs[0]:
        num += 1
        
        state = graphs[0].nodes[id]['polygon_name']
        ts_population_0000 = []
        ts_population_0800 = []
        ts_population_1600 = []
        
        #cheating
        for graph in graphs:
            if(graph.graph['date_time'].hour == 0): 
                ts_population_0000.append(graph.nodes[id]['population'])
                continue
            if(graph.graph['date_time'].hour == 8): 
                ts_population_0800.append(graph.nodes[id]['population'])
                continue
            if(graph.graph['date_time'].hour == 16): 
                ts_population_1600.append(graph.nodes[id]['population'])
                if(graph.graph['date_time'] == pd.Timestamp('2020-12-12 16')):
                    ts_population_0000.append(None)
                continue
        '''
        for graph_0000, graph_0800, graph_1600  in zip(graphs[::3], graphs[1::3], graphs[2::3]):
            ts_population_0000.append(graph_0000.nodes[id]['population'])
            ts_population_0800.append(graph_0800.nodes[id]['population'])
            ts_population_1600.append(graph_1600.nodes[id]['population'])
        '''
        print(len(ts_population_0000), len(ts_population_0800), len(ts_population_1600), len(ts_scale))
        
        concat = ts_population_0000 + ts_population_0800 + ts_population_1600
        ind = concat.index(None)
        minimum, maximum = min(concat[:ind] + concat[ind+1:]), max(concat[:ind] + concat[ind+1:])

        df = pd.DataFrame({
            'date':                   np.array(ts_scale),
            '00:00 UTC to 08:00 UTC': np.array(ts_population_0000),
            '08:00 UTC to 16:00 UTC': np.array(ts_population_0800),
            '16:00 UTC to 00:00 UTC': np.array(ts_population_1600),
        })
        
        plt.subplot(4,4, num)
        plt.plot(df['date'], df['00:00 UTC to 08:00 UTC'], marker='', color=palette(1), alpha=0.9, label='00:00 UTC to 08:00 UTC')
        plt.plot(df['date'], df['08:00 UTC to 16:00 UTC'], marker='', color=palette(2), alpha=0.9, label='08:00 UTC to 16:00 UTC')
        plt.plot(df['date'], df['16:00 UTC to 00:00 UTC'], marker='', color=palette(3), alpha=0.9, label='16:00 UTC to 00:00 UTC')
        
        plt.ylim(minimum*0.95, maximum*1.05)
        plt.title(state, loc='center', fontsize=12, fontweight=0, color=palette(1))
        
        if num in range(1, 16, 4):
            plt.ylabel('Facebook population in thousands')
        if num in range(1, 13) :
            plt.tick_params(labelbottom=False)
        
        x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
        plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: int(y/1000)))
    
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, fontsize=20)
    
    if(store):       
        fig.savefig(name, dpi=320)
    else:
        plt.show()

    return fig

# Change position based slicing to date slicing, add timeframe slicing
def plot_nation_population(graphs: List[Graph], start_date: str = '2020-03-25', store: bool = False, name: str = 'nation-population-plot.png'):
    '''    
    Generates plot of total Facebook population on national level over time.

    Args:
        graphs:     list of administrative population graphs
        start_date: date-time string of first graph showing on x-axis
        store:      discards/saves plot as <name>
        name:       name of stored file
        
    Returns:
        fig: resulting graph-figure
    '''
    ts_population = []
    for graph_0000, graph_0800, graph_1600 in zip(graphs[::3], graphs[1::3], graphs[2::3]):
        population = 0
        for id in graph_0000:
            avg = graph_0000.nodes[id]['population'] + graph_0800.nodes[id]['population'] + graph_1600.nodes[id]['population']
            population += avg
        ts_population.append(population/3)
        
    curr_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    ts_scale  = []
    for i in range(len(ts_population)):
        ts_scale.append(curr_date)
        curr_date += pd.Timedelta(days=1)
    
    df = pd.DataFrame({
            'date':       np.array(ts_scale),
            'population': np.array(ts_population),
        })
        
    fig = plt.figure()
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
        
    plt.plot(df['date'], df['population'], marker='', color=palette(1), alpha=0.9)
    
    minimum, maximum = min(ts_population), max(ts_population)
    plt.ylim(minimum*0.95, maximum*1.05)
    plt.title('Daily Facebook population - national average', loc='center', fontsize=12, fontweight=0, color=palette(1))
    
    x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
    plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.ylabel('Facebook population in millions')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: y/1000000))
    
    if(store):       
        fig.savefig(name, dpi = 320)
    else:
        plt.show()

    return fig

# Use 8 hour timeframe instead of days as slice and replace plot_nation_population()?
def plot_nation_population_time_aggregate(graphs: List[Graph], start_date: str = '2020-03-25', slice: int = 7, store: bool = False, name: str = 'nation-population-time-aggregate-plot.png'):
    '''    
    Generates plot of time aggregated Facebook population on national level over time (default: 1 week aggregate).

    Args:
        graphs:     list of administrative population graphs
        start_date: date-time string of first graph showing on x-axis
        slice:      aggregation over <slice> days (default: 7 days)
        store:      discards/saves plot as <name>
        name:       name of stored file
        
    Returns:
        fig: resulting graph-figure
    '''
    agg_graphs = con.time_aggregate_admin_population_graph(graphs, slice = slice*3)
    
    ts_population = []
    for graph in agg_graphs:
        population = 0
        for id in graph:
            population += graph.nodes[id]['population']
        ts_population.append(population/(slice*3))
        
    curr_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    ts_scale  = []
    for i in range(len(ts_population)):
        ts_scale.append(curr_date)
        curr_date += pd.Timedelta(days=slice)
    
    df = pd.DataFrame({
            'date':       np.array(ts_scale),
            'population': np.array(ts_population),
        })
        
    fig = plt.figure()
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
        
    plt.plot(df['date'], df['population'], marker='', color=palette(1), alpha=0.9)
    
    minimum, maximum = min(ts_population), max(ts_population)
    plt.ylim(minimum*0.95, maximum*1.05)
    plt.title(f'Facebook population - national {slice} day average', loc='center', fontsize=12, fontweight=0, color=palette(1))
    
    x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
    plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.ylabel('Facebook population in millions')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: y/1000000))
    
    if(store):       
        fig.savefig(name, dpi = 320)
    else:
        plt.show()

    return fig

# Change position based slicing to date slicing, add timeframe slicing
def plot_state_population_share(graphs: List[Graph], start_date: str = '2020-03-25', store: bool = False, name: str = 'state-population-share-plot.png', equalize: bool = False):
    '''    
    Generates plot of relative share of Facebook population on national level over time for each state.

    Args:
        graphs:     list of administrative population graphs
        start_date: date-time string of first graph showing on x-axis
        store:      discards/saves plot as <name>
        name:       name of stored file
        equalize:   use equal y-axis in plot 
        
    Returns:
        fig: resulting graph-figure
    '''
    fig = plt.figure(figsize=(32, 18))
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    
    graphs = con.time_aggregate_admin_population_graph(graphs, slice = 3)
    
    curr_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    ts_scale  = []
    for i in range(len(graphs)):
        ts_scale.append(curr_date)
        curr_date += pd.Timedelta(days=1)
    
    num = 0
    for id in graphs[0]:
        num += 1
        
        state = graphs[0].nodes[id]['polygon_name']
        
        ts_share = []
        for graph in graphs:
            total_population = 0
            for node in graphs[0]:
                total_population += graph.nodes[node]['population']
        
            ts_share.append(graph.nodes[id]['population'] / total_population)
        
        minimum, maximum = min(ts_share), max(ts_share)
        if(equalize):
            minimum = 0
            maximum = 0.235
        
        df = pd.DataFrame({
            'date':  np.array(ts_scale),
            'share': np.array(ts_share),
        })
        
        plt.subplot(4,4, num)
        plt.plot(df['date'], df['share'], marker='', color=palette(1), alpha=0.9, label='00:00 UTC to 08:00 UTC')
        
        plt.ylim(minimum*0.95, maximum*1.05)
        plt.title(state, loc='center', fontsize=12, fontweight=0, color=palette(1))
        
        if num in range(1, 16, 4):
            plt.ylabel('Population share')
        if num in range(1, 13) :
            plt.tick_params(labelbottom=False)
        
        x_dates = df['date'].dt.strftime('%Y-%m-%d').sort_values().unique()
        plt.gca().set_xticklabels(labels=x_dates, rotation=45, ha='right')
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:.1%}'.format(y)))
    
    if(store):       
        fig.savefig(name, dpi=320)
    else:
        plt.show()

    return fig
    
if __name__ == '__main__':
    #plot_basic_SIR(997, 3, 0, 0.4, 0.04, 100, 'days', True)
    pass