# src/build_graph.py
import networkx as nx
import json
from typing import List, Dict

def build_graph_from_events(events: List[Dict]) -> nx.DiGraph:
    """
    Construire un DiGraph où les noeuds sont des hosts (prefix 'host:').
    Les arêtes entre hosts ont un attribut 'events' (liste d'événements).
    """
    G = nx.DiGraph()
    for ev in events:
        src = ev.get("src_ip") or "unknown"
        dst = ev.get("dst_ip") or "unknown"
        node_src = f"host:{src}"
        node_dst = f"host:{dst}"
        G.add_node(node_src, type="host")
        G.add_node(node_dst, type="host")
        # Edge key: si exist, append, sinon créer
        if G.has_edge(node_src, node_dst):
            G[node_src][node_dst]["events"].append({
                "action": ev.get("action"),
                "ts": ev.get("timestamp"),
                "user": ev.get("user"),
                "raw": ev.get("raw")
            })
        else:
            G.add_edge(node_src, node_dst, events=[{
                "action": ev.get("action"),
                "ts": ev.get("timestamp"),
                "user": ev.get("user"),
                "raw": ev.get("raw")
            }])
    return G

def save_graph_gml(G: nx.DiGraph, out_path: str):
    nx.write_gml(G, out_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python build_graph.py events.json out_graph.gml")
    else:
        ev_path = sys.argv[1]
        out = sys.argv[2]
        with open(ev_path, "r", encoding="utf-8") as f:
            events = json.load(f)
        G = build_graph_from_events(events)
        save_graph_gml(G, out)
        print(f"Graph saved to {out} with {len(G.nodes())} nodes and {len(G.edges())} edges")
