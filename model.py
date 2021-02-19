import copy
import plot
import settings
import sys
import construction as con
import networkx as nx
import numpy as np
from   typing  import List, Set, Dict, Tuple, Optional
from networkx import Graph, DiGraph

####################################################################
### Disclaimer - paused because of                               ###
### problems with mobility movement data set. Will be revisited. ###
####################################################################

def init_state_SIR(date: str): -> List[Set[Tuple]]
    '''
    Returns list with initial distribution of infected, susceptible, recovered as share of total state population.
    
    Args:
        date: initial date (format 'YYYY-MM-DD')
        
    Returns:
        init_distribution: list with initial distribution of infected, susceptible, recovered as share of total state population for each state.
    '''
    state_population = {
        'Baden-Württemberg': 11100394,
        'Bayern': 13124737,
        'Berlin': 3669491,
        'Brandenburg': 2521893,
        'Bremen': 681202,
        'Hamburg': 1847253,
        'Hessen': 6288080,
        'Mecklenburg-Vorpommern': 1608138,
        'Niedersachsen': 7993608,
        'Nordrhein-Westfalen': 17947221,
        'Rheinland-Pfalz': 4093903,
        'Saarland': 986887,
        'Sachsen': 4071971,
        'Sachsen-Anhalt': 2194782,
        'Schleswig-Holstein': 2903773,
        'Thüringen': 2133378,
    }
    
    init_distribution = {}
    for state in state_population.keys():
        population           = state_population[state]
        currently_infected   = con.currently_infected(date, Bundesland = state)
        cumulated_recovered  = con.cumulated_recovered(end_date = date, Bundesland = state)
        cumulated_dead       = con.cumulated_dead(end_date = date, Bundesland = state)
        
        rel_infected    = currently_infected / population
        rel_recovered   = (cumulated_recovered + cumulated_dead) / population
        rel_susceptible = 1 - rel_infected - rel_recovered
        
        init_distribution[state] = {'rel_susceptible': rel_susceptible, 'rel_infected': rel_infected, 'rel_recovered': rel_recovered}
    return init_distribution
        
def closed_SIR(susceptible: int, infected: int, recovered: int, infection_rate: float, recovery_rate: float, timeframe: int) -> Tuple[List[float]]:
    '''
    Simulation of the most basic SIR model.

    Args:
        susceptible:    initial number of susceptible individuals (S)
        infected:       initial number of infected    individuals (I)
        recovered:      initial number of recovered   individuals (R)
        infection_rate: number of new contagion of an infected individual per time step (beta)
        recovery_rate:  rate, at which an infected individual either dies or recovers (gamma)
        
    Returns:
        ts_susceptible: time series of susceptible individuals
        ts_infected:    time series of infected individuals
        ts_recovered:   time series of recoverd individuals
        ts_scale:       time series of time steps
    '''
        
    ts_susceptible = [susceptible]
    ts_infected    = [infected]
    ts_recovered   = [recovered]
    ts_scale       = [step for step in range(0, timeframe + 1)]

    for step in ts_scale[1:]:
        population = susceptible + infected + recovered
        
        delta_susceptible = -infection_rate * susceptible * infected / population
        delta_infected    = infection_rate  * susceptible * infected / population - recovery_rate * infected
        delta_recovered   = recovery_rate   * infected
        
        susceptible += delta_susceptible
        infected    += delta_infected
        recovered   += delta_recovered
        
        ts_susceptible.append(susceptible)
        ts_infected.append(infected)
        ts_recovered.append(recovered)
        
    return ts_susceptible, ts_infected, ts_recovered, ts_scale

# Fix: type(Graph.graph['date_time']) = pandas.Timestamp() now, not str
def static_state_SIR(graph, infection_rate, recovery_rate, timeframe) -> Graph:
    '''
    Closed SIR-simulation for each node of Graph, initialised with RKI data.
    
    Args:
        graph:          administrative population graph
        infection_rate: number of new contagion of an infected individual per time step (beta)
        recovery_rate:  rate, at which an infected individual either dies or recovers (gamma)
        timeframe:      number of timesteps used for SIR simulation
    
    Returns:
        ts_graph: Graph whose nodes carrying time series of susceptible, infected, recovered
    
    '''
    
    ts_graph          = copy.deepcopy(nx.create_empty_copy(graph))
    date_time         = ts_graph.graph['date_time']
    init_distribution = init_state_SIR(date_time[:10])
    
    for id in graph:
        state  = graph.nodes[id]['polygon_name']
        fb_pop = graph.nodes[id]['population']
        
        init_susceptible = fb_pop * init_distribution[state]['rel_susceptible']
        init_infected    = fb_pop * init_distribution[state]['rel_infected']
        init_recovered   = fb_pop * init_distribution[state]['rel_recovered']
        
        ts_susceptible, ts_infected, ts_recovered, ts_scale = closed_SIR(init_susceptible, init_infected, init_recovered, infection_rate, recovery_rate, timeframe)
        
        ts_graph.graph['ts_scale']           = ts_scale
        ts_graph.nodes[id]['ts_susceptible'] = ts_susceptible
        ts_graph.nodes[id]['ts_infected']    = ts_infected
        ts_graph.nodes[id]['ts_recovered']   = ts_recovered
        
    return ts_graph
    
# Ignore, unfinished, untested. SIR-model with moving population on tile level using tile level movement graphs.
'''            
# needs testing
def dynamic_state_SIR(graphs, infection_rate, recovery_rate, timeframe):

    def init_edges(graph: Graph) -> Dict:
        init_distribution = {}
        for id in graph:
            susceptible = ts_graph.nodes[id]['ts_susceptible'][-1]
            infected    = ts_graph.nodes[id]['ts_infected'][-1]
            recovered   = ts_graph.nodes[id]['ts_recovered'][-1]
            population  = graph.nodes[id]['population'] 
            
            rel_susceptible = susceptible / graph.nodes[id]['population'] 
            rel_infected    = infected    / graph.nodes[id]['population']       
            rel_recovered   = recoverd    / graph.nodes[id]['population'] 
            
            init_distribution[id] = {'rel_susceptible': rel_susceptible, 'rel_infected': rel_infected, 'rel_recovered': rel_recovered}
            
        return init_distribution
    
    # copy graph, no changes
    graphs   = list(map(copy.deepcopy, graphs))
    ts_graph = copy.deepcopy(nx.create_empty_copy(graphs[0]))
    
    # Build ts_scale
    if(timeframe >= len(graphs)): timeframe = len(graphs) - 1
    ts_graph.graph['ts_scale'] = [step for step in range(0, timeframe + 1)]
    
    # innit ts_graph
    init = init_state_SIR(date)
    for id in ts_graph:
        state  = ts_graph.nodes[id]['polygon_name']
        fb_pop = ts_graph.nodes[id]['population']
        
        init_susceptible = fb_pop * init[state]['rel_susceptible']
        init_infected    = fb_pop * init[state]['rel_infected']
        init_recovered   = fb_pop * init[state]['rel_recovered']
        
        ts_graph.nodes[id]['ts_susceptible'] = [init_susceptible]
        ts_graph.nodes[id]['ts_infected']    = [init_infected]
        ts_graph.nodes[id]['ts_recovered']   = [init_recovered]
    # ----------------------------
    for i in range(1, timeframe):
        init = init_edges(graphs[i])
        for id in ts_graph:
            for source, target in graphs[i].in_edges(id):
                

                
    
    #---------------------------
            
            # first exchange (in and out), then SIR step
            
            #(sum ins - outs) * state average
            #add to last sir
            #update
            #repeat
            for source, target in curr.in_edges(id):
                n_edge = curr.edges[(source, target)]['n_crisis']
                last_susceptible = last.nodes[source]['susceptible']
                last_infected    = last.nodes[source]['infected']
                last_recovered   = last.nodes[source]['recovered']
                last_population  = last.nodes[source]['population']
                
                edge_susceptible = n_edge * last_susceptible / last_population
                edge_infected    = n_edge * last_infected    / last_population
                edge_recovered   = n_edge * last_recovered   / last_population
                edge_population  = n_edge
                
                susceptible += edge_susceptible
                infected    += edge_infected
                recovered   += edge_recovered
                population  += edge_population
            
            # SIR step            
            delta_susceptible = -infection_rate * susceptible * infected / population
            delta_infected    = infection_rate  * susceptible * infected / population - recovery_rate * infected
            delta_recovered   = recovery_rate   * infected
            
            susceptible += delta_susceptible
            infected    += delta_infected
            recovered   += delta_recovered
            
            # update
            curr.nodes[id]['susceptible'] = susceptible
            curr.nodes[id]['infected']    = infected
            curr.nodes[id]['recovered']   = recovered
            curr.nodes[id]['population']  = population
    
    return graphs
'''
   
    
'''
#create graph with nodes
# initiate with rki data
# simulate
'''  