# build_graph.py
import networkx as nx
from parse_logs import parse_file
import matplotlib.pyplot as plt

def build_graph_from_df(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        ts = row['ts']
        user = row['user']
        action = row['action']
        # nodes: user, ip src, ip dst, file
        G.add_node(user, type='user')
        if row.get('src'):
            G.add_node(row['src'], type='ip')
            G.add_edge(row['src'], user, label='src_of', ts=ts, action=action)
        if row.get('dst'):
            G.add_node(row['dst'], type='ip')
            G.add_edge(user, row['dst'], label=action, ts=ts)
        if row.get('file'):
            G.add_node(row['file'], type='file')
            G.add_edge(user, row['file'], label=action, ts=ts)
        # also connect user->action as a node optionally
    return G

def draw_graph(G, out="graph.png"):
    pos = nx.spring_layout(G)
    labels = {n: n for n in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"Saved graph to {out}")

if __name__ == "__main__":
    df = parse_file("../data/sample_logs.txt")
    G = build_graph_from_df(df)
    draw_graph(G)

