#! /bin/python3
import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import utils

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
        s = 0
        for neighbor in neighbors:
            if G.nodes[neighbor]['state'] == 1:
                s += 1
        G.nodes[node]['risk_perception'] = np.exp(-(H + J * s / k))
        #print(G.nodes[node]['risk_perception'])

def spread(G: nx.Graph, tau: float) -> None:
    """
    Propagate the disease in the graph G with probability tau*risk_perception
    """
    
    for node in G.nodes():
        
        neighbors = list(G.neighbors(node))
        s = 0
        for neighbor in neighbors:
            if G.nodes[neighbor]['state'] == 1:
                s += 1
                
        if G.nodes[node]['state'] == 1:
            G.nodes[node]["tmp"] = 0
            continue
        elif s == 0:
            continue
        else:
            if np.random.random() < tau * G.nodes[node]['risk_perception']:
                G.nodes[node]['state'] = 1
                G.nodes[node]["tmp"] = 1
                
def recover(G: nx.Graph, gamma: float) -> None:
    """
    Recover the infected nodes with probability gamma
    """
    
    for node in G.nodes():
        if G.nodes[node]['state'] == 1: #and G.nodes[node]["tmp"] == 0:
            if np.random.random() < gamma:
                G.nodes[node]['state'] = 0

def simulate_disease_spread(
    G: nx.Graph, 
    H: float, 
    J: float, 
    tau: int = 0.1, 
    gamma: int = 0.1, 
    iteration: int = 100,
    initial_infected: int = 10,
    plot: bool = False
    ) -> list[float]:
    """
    Simulates the spread of a deseas over a graph
    """

    initialize_infected(G, initial_infected)
    d = dict(G.degree)
    
    if plot:
        position = nx.kamada_kawai_layout(G)
        fig, ax = plt.subplots()  
        
    infected = []  
    
    for i in range(iteration):
        utils.progress_bar(i, iteration)

        if plot:
            color_map = []
            for node in G:
                if G.nodes[node]['state'] == 0:
                    color_map.append('blue')
                else:
                    color_map.append('red')

            ax.clear()
            nx.draw(G, ax=ax, node_size=[v*10 for v in d.values()], node_color=color_map, with_labels=False, width=0.1, pos=position) 
            plt.pause(1)
            
        infected.append(count_infected(G)/G.number_of_nodes())
        
        # At each iteration, evaluate the risk perception of each node, propagate the disease and recover the infected nodes
        evaluate_risk_perception(G = G, H = H, J = J)
        spread(G, tau=tau)
        recover(G, gamma=gamma)
        
    return infected
        
def generate_information_network(physical_net: nx.Graph, virtual_net: nx.Graph, q: float) -> nx.Graph:
    """
    Generate the information network from the physical network and the virtual network
    """
    info_net = nx.DiGraph()
    info_net.add_nodes_from(physical_net.nodes())
    
    for node in physical_net.nodes():
        neighbors = list(physical_net.neighbors(node))
        for neighbor in neighbors:
            if np.random.random() < (1 - q):
                info_net.add_edge(node, neighbor)
                
    for node in virtual_net.nodes():
        neighbors = list(virtual_net.neighbors(node))
        for neighbor in neighbors:
            if np.random.random() < q:
                info_net.add_edge(node, neighbor)
    
    return info_net
    
def plot_vir_phis_info():
    
    nodes = 15
    m = 2
    physical = nx.barabasi_albert_graph(nodes, m)
    initialize_infected(physical, 3)
    fig, axs = plt.subplots(1, 3)
    axs[0].set_title("Physical Network")
    axs[1].set_title("Virtual Network")
    axs[2].set_title("Information Network")

    virtual = nx.barabasi_albert_graph(nodes, m)

    information = generate_information_network(physical, virtual, 0.5)

    d = dict(physical.degree)  
    position = nx.kamada_kawai_layout(physical)

    nx.draw(physical, ax=axs[0], node_size= 250, node_color = "orange",  with_labels=True, width=1, pos=position)   
    nx.draw(virtual, ax=axs[1], node_size= 250, with_labels=True, node_color = "cornflowerblue", width=1, pos=position) 
    nx.draw(information, ax=axs[2], node_size= 250, with_labels=True, width=1, node_color = "forestgreen", pos=position, arrows=True, arrowsize=15, arrowstyle='-|>')
    plt.show()
    
def main():
        
    plot_vir_phis_info()
    
if __name__ == "__main__":
    main()
