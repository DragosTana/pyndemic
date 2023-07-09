import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import tqdm
from matplotlib.animation import FuncAnimation

#------------- Barabasi-Albert Graph -------------#

    # Mean connectivty for BA model: <k> = 2m
    # Degree distribution: P(k) ~ 2 m^2 k^(-3)
    # Gamma = 3

def plot_degree_distribution(G: nx.Graph) -> None:
    """
    Plot the degree distribution of a graph G
    """
    
    degrees = [degree for node, degree in G.degree()]
    plt.hist(degrees, bins = 30, density = True)
    k = np.arange(1, max(degrees), 1)
    p = 8 / (k**(3))
    #plt.plot(k, p, 'r--', linewidth = 2)
    plt.show()
    
def plot_graph(G: nx.Graph) -> None:
    """
    plot a graph G. The nodes are colored blue if they are susceptible and red if they are infected.
    """
    
    fig, ax = plt.subplots()
    color_map = []
    for node in G:
        if G.nodes[node]['state'] == 0:
            color_map.append('blue')
        else:
            color_map.append('red')
    nx.draw(G, ax = ax, node_size = 20, node_color = color_map, with_labels = False, width = 0.1)
    plt.show()    

def initialize_infected(G: nx.Graph, n: int = 10) -> None:
    """
    Given a graph G, initialize n nodes to be infected
    """
    
    number_of_nodes = G.number_of_nodes()
    infected = rd.sample(range(number_of_nodes), n)
    for node in G.nodes():
        if node in infected:
            G.nodes[node]['state'] = 1
            G.nodes[node]["tmp"] = 1
        else:
            G.nodes[node]['state'] = 0
            G.nodes[node]["tmp"] = 0
            
def count_infected(G: nx.Graph) -> int:
    """
    Count the number of infected nodes in a graph G
    """
    
    c = 0
    for node in G.nodes():
        if G.nodes[node]['state'] == 1:
            c += 1
    return c
    
def evaluate_risk_perception(G: nx.Graph, H: float, J: float) -> None:
    """
    Function to evaluate the risk perception of each node in the graph G
    """
    
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        k = len(neighbors)
        s = np.count_nonzero([G.nodes[neighbor]['state'] for neighbor in neighbors])
        G.nodes[node]['risk_perception'] = np.exp(-(H + J * s / k))
               
def spread(G: nx.Graph, tau: int) -> None:
    """
    Propagate the disease in the graph G with probability p*risk_perception
    """
    
    for node in G.nodes():
        if G.nodes[node]['state'] == 1:
            G.nodes[node]["tmp"] = 0
            continue
        elif np.count_nonzero([G.nodes[neighbor]['state'] for neighbor in G.neighbors(node)]) == 0:
            continue
        else:
            if np.random.random() < tau * G.nodes[node]['risk_perception']:
                G.nodes[node]['state'] = 1
                G.nodes[node]["tmp"] = 1
                
def recover(G: nx.Graph, gamma: int) -> None:
    """
    Recover the infected nodes with probability gamma
    """
    
    for node in G.nodes():
        if G.nodes[node]['state'] == 1 and G.nodes[node]["tmp"] == 0:
            if np.random.random() < gamma:
                G.nodes[node]['state'] = 0

       
def simulate_disease_spread(G: nx.Graph, H: float, J: float, tau: int = 0.1, gamma: int = 0.3, iteration: int = 100) -> None:
    
    initialize_infected(G, len(G.nodes()) // 10)
    
    fig, ax = plt.subplots()    
    
    for i in range(iteration):

        evaluate_risk_perception(G, H, J)
        spread(G, tau)
        recover(G, gamma)
        
        color_map = []
        for node in G:
            if G.nodes[node]['state'] == 0:
                color_map.append('blue')
            else:
                color_map.append('red')
        
        nx.draw(G, ax = ax, node_size = 20, node_color = color_map, with_labels = False, width = 0.1)
        ax.clear()
    plt.show()    
            
     
def main():
    # Create a BA graph
    nodes = 1000
    m = 2
    G = nx.barabasi_albert_graph(nodes, m)
    
    # initilize infected nodes
    initial_infected = 5
    initialize_infected(G, 3)
    
    # robe per plottare
    d = dict(G.degree)
    position = nx.kamada_kawai_layout(G)
    fig, ax = plt.subplots()    
    
    # Inizio simulazione
    for i in range(300):
        # At each iteration, evaluate the risk perception of each node, propagate the disease and recover the infected nodes
        evaluate_risk_perception(G, H=1, J=0.1)
        spread(G, tau=0.2)
        recover(G, gamma=0.1)
        
        # roba per plottare
        color_map = []
        for node in G:
            if G.nodes[node]['state'] == 0:
                color_map.append('blue')
            else:
                color_map.append('red')
                
        ax.clear()
        nx.draw(G, ax=ax, node_size=[v*10 for v in d.values()], node_color=color_map, with_labels=False, width=0.1, pos=position) 
        plt.pause(0.1)  
        
    fig.show()
        


main()






         
         