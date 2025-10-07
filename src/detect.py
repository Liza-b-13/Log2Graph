# src/detect.py
import json
import networkx as nx
from typing import List, Dict

def load_kb(kb_path: str) -> List[Dict]:
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def edge_latest_action(G: nx.DiGraph, u: str, v: str):
    """
    Renvoie l'action la plus récente enregistrée sur l'arête u->v
    (on prend le dernier événement de la liste).
    """
    evs = G[u][v].get("events", [])
    if not evs:
        return None
    return evs[-1].get("action")

def path_action_sequence(G: nx.DiGraph, path: List[str]) -> List[str]:
    """
    Pour un chemin (liste de noeuds), renvoie la séquence d'actions
    correspondantes aux arêtes successives.
    """
    seq = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        action = edge_latest_action(G, u, v)
        seq.append(action or "unknown")
    return seq

def sequence_matches(pattern: List[str], seq: List[str]) -> bool:
    """
    Vérifie si la liste `pattern` est une sous-séquence contiguë de `seq`.
    Simple recherche de sous-liste.
    """
    n = len(pattern)
    for i in range(len(seq) - n + 1):
        if seq[i:i+n] == pattern:
            return True
    return False

def detect_patterns_in_graph(G: nx.DiGraph, kb: List[Dict], max_path_len: int = 5):
    alerts = []
    for pattern in kb:
        pat_seq = pattern.get("sequence", [])
        # parcours simple : pour chaque paire de noeuds, chercher chemins courts
        for source in G.nodes():
            # limiter la recherche: chemins de longueur <= max_path_len
            for target in G.nodes():
                if source == target:
                    continue
                for path in nx.all_simple_paths(G, source=source, target=target, cutoff=max_path_len):
        # reste du code
                    if len(path) < 2:
                        continue
                    seq = path_action_sequence(G, path)
                    if sequence_matches(pat_seq, seq):
                        alerts.append({
                            "pattern_id": pattern.get("id"),
                            "pattern_name": pattern.get("name"),
                            "path": path,
                            "actions_sequence": seq
                        })
    return alerts

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python detect.py graph.gml data/kb_patterns.json")
    else:
        graph_path = sys.argv[1]
        kb_path = sys.argv[2]
        G = nx.read_gml(graph_path)
        kb = load_kb(kb_path)
        alerts = detect_patterns_in_graph(G, kb)
        print("Alerts:", alerts)
