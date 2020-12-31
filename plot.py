import analytics
import simplekml
import matplotlib as plt
import model    as md
import networkx as nx
import numpy    as np
import pandas   as pd
import seaborn  as sns
import utility  as ut
from networkx   import Graph

def tile_kml(graph: Graph, path: str):
    '''
    Generates a KML-file showing the outlines of every tile at geospatial position.
    For quick viewing use https://ivanrublev.me/kml/

    Args:
        graph: Graph object
        path:  Path pointing to storage directory
    '''
    kml = simplekml.Kml()
    kml.document.name = 'BLUBB'
    for node in graph.nodes:
        p0, p1, p2, p3 = analytics.get_tile_vertices(graph.nodes[node]['lon'], graph.nodes[node]['lat'], graph.graph['tile_size'])
        pol = kml.newpolygon(name=node)
        pol.outerboundaryis = [p0, p1, p3, p2, p0]
        pol.style.polystyle.color = simplekml.Color.red
        pol.style.polystyle.outline = 1
    kml.save(path + '.kml')
   
def plot_SIR(susceptible, infected, recovered, infection_rate, recovery_rate, timeframe, time_unit = 'days', store = False) -> plt.axes.Axes:
    '''
    Creates and saves a plot of susceptible, infected and recovered people over time of an SIR-model.

    Args:
        susceptible:    initial number of people that can be infected
        infected:       initial number of people that are infected
        recovered:      initial number of people that cannot be infected
        infection_rate: number of people that one infected person infects per time step
        recovery_rate:  rate, at which infected people recover
        
    Returns:
        plot: "plot object" of SIR dynamics (need to look up type)
    '''
    susceptible_data, infected_data, recovered_data, timeframe_data = md.closed_SIR(susceptible, infected, recovered, infection_rate, recovery_rate, timeframe = 100)
    
    data_preproc = pd.DataFrame({
        time_unit:     timeframe_data,
        'Susceptible': susceptible_data,
        'Infected':    infected_data,
        'Recovered':   recovered_data,
    })
    
    sns.set_theme()
    sns.set(style='darkgrid')
    plot = sns.lineplot(x=time_unit, y='value', hue='variable', data=pd.melt(data_preproc, [time_unit]))
    
    if(store):
        fig = plot.get_figure()
        fig.savefig('output.png')
    
    return plot
    
if __name__ == '__main__':
    #plot_basic_SIR(997, 3, 0, 0.4, 0.04, 100, 'days', True)
    pass