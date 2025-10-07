# src/visualize.py
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, figsize=(8,6)):
    """
    Retourne une figure matplotlib affichant le graphe G.
    """
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.axis('off')
    fig = plt.gcf()
    return fig
