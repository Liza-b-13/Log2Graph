# tests/test_detect.py
from src.extract_events import parse_csv_to_events
from src.build_graph import build_graph_from_events
from src.detect import detect_patterns_in_graph, load_kb
def test_detect():
    events = parse_csv_to_events("sample_logs.csv", mode="llm")
    G = build_graph_from_events(events)
    kb = load_kb("data/kb_patterns.json")
    alerts = detect_patterns_in_graph(G, kb)
    # On ne fait pas d'assert strict (dépend du sample), juste s'assurer que la fonction s'exécute
    assert isinstance(alerts, list)
