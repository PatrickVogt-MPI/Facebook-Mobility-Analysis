import sys
import construction as con
import numpy as np

def closed_SIR (susceptible: int, infected: int, recovered: int, infection_rate: float, recovery_rate: float, timeframe: int):
    '''
    Simulation of a simple SIR model.

    Args:
        susceptible:    initial number of susceptible individuals (S)
        infected:       initial number of infected    individuals (I)
        recovered:      initial number of recovered   individuals (R)
        infection_rate: number of new contagion of an infected individual per time step (beta)
        recovery_rate:  rate, at which an infected individual either dies or recovers (gamma)
        
    Returns:
        XXX
    '''
    susceptible_data = [susceptible]
    infected_data    = [infected]
    recovered_data   = [recovered]
    time_data        = [step for step in range(0, timeframe + 1)]

    for step in time_data[1:]:
        population = susceptible + infected + recovered
        
        delta_susceptible = -infection_rate * susceptible * infected / population
        delta_infected    = infection_rate  * susceptible * infected / population - recovery_rate * infected
        delta_recovered   = recovery_rate   * infected
        
        susceptible += delta_susceptible
        infected    += delta_infected
        recovered   += delta_recovered
        
        susceptible_data.append(susceptible)
        infected_data.append(infected)
        recovered_data.append(recovered)
        
    return np.array(susceptible_data), np.array(infected_data), np.array(recovered_data), np.array(time_data)
    
def state_SIR(path, graphs, infection_rate, recovery_rate, timeframe = None):
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
    
    init_graph     = graphs[0]
    init_date_time = init_graph.graph['date_time']
    
    for id in init_graph:
        state         = init_graph.nodes[id]['polygon_name']
        fb_population = init_graph.nodes[id]['population']
        population    = state_population[state]
        infected      = con.currently_infected(path, date_time, Bundesland=state)
        
        graph.nodes[id]['susceptible'] = fb_pop * (1 - infected / population)
        graph.nodes[id]['infected']    = fb_pop * infected / population
        graph.nodes[id]['recovered']   = 0
    
    for curr, last in zip(graphs[1:], graphs[:-1]):
        for id in last:
            susceptible = last.nodes[id]['susceptible']
            infected    = last.nodes[id]['infected']
            recovered   = last.nodes[id]['recovered']
            population  = last.nodes[id]['population']
            
            # first exchange, then SIR step
            for source, target in curr.in_edges(id):
                n_edge = curr.edges[source][target]['n_crisis']
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
                
            delta_susceptible = -infection_rate * susceptible * infected / population
            delta_infected    = infection_rate  * susceptible * infected / population - recovery_rate * infected
            delta_recovered   = recovery_rate   * infected
            
            susceptible += delta_susceptible
            infected    += delta_infected
            recovered   += delta_recovered
            
            curr.nodes[id]['susceptible'] = susceptible
            curr.nodes[id]['infected']    = infected
            curr.nodes[id]['recovered']   = recovered
            curr.nodes[id]['population']  = population
    
    return graphs
    
def county_SIR():
    pass

def tile_SIR():
    pass
    
if __name__ == '__main__':
    sys.stdout = open('output.txt', 'w')
    
    