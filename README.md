# Log2Graph — prototype LLM-friendly pour la détection d'intrusion

## But
Montrer comment on peut extraire des événements depuis des logs, les structurer en un graphe d'événements (attack graph) et utiliser un petit modèle NLP pour aider à filtrer les événements suspects.

## Contenu
- `data/sample_logs.txt` : logs d'exemple
- `src/parse_logs.py` : parseur simple vers DataFrame
- `src/build_graph.py` : construction et visualisation du graphe (networkx)
- `src/detect_suspicious.py` : démonstration d'un classifieur NLP (proxy)
- `src/visualize_graph.py` : script pour sauver l'image du graphe

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

