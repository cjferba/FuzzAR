"""
fuzzy_visualization.py

Este módulo proporciona herramientas para visualizar reglas de asociación difusas como grafos.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_json(path):
    with open(path) as f:
        data = json.load(f)
    return nx.node_link_graph(data)

def plot_graph(G):
    pos = nx.spring_layout(G)
    rule_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "rule"]
    item_nodes = [n for n in G.nodes if n not in rule_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=item_nodes, node_color="skyblue", node_shape="o", label="Item")
    nx.draw_networkx_nodes(G, pos, nodelist=rule_nodes, node_color="salmon", node_shape="s", label="Rule")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.legend()
    plt.title("Grafo de Reglas Difusas")
    plt.show()
