
import json
import networkx as nx
import matplotlib.pyplot as plt


def load_graph_from_json(json_path):
    with open(json_path, 'r') as f:
        graph_data = json.load(f)
    G = nx.node_link_graph(graph_data)
    return G


def plot_graph(G, figsize=(10, 8)):
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    node_shapes = {}
    labels = {}

    for node, data in G.nodes(data=True):
        node_type = data.get("type", "")
        labels[node] = node
        if node_type == "item":
            node_colors.append("skyblue")
            node_shapes[node] = "o"
        elif node_type == "rule":
            node_colors.append("salmon")
            node_shapes[node] = "s"
        else:
            node_colors.append("lightgray")
            node_shapes[node] = "o"

    # Draw different shapes
    unique_shapes = set(node_shapes.values())
    for shape in unique_shapes:
        nodes_with_shape = [node for node in G.nodes if node_shapes[node] == shape]
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=nodes_with_shape,
            node_color=[node_colors[list(G.nodes).index(n)] for n in nodes_with_shape],
            node_shape=shape,
            node_size=800,
        )

    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Grafo de Reglas Difusas")
    plt.axis("off")
    plt.show()
