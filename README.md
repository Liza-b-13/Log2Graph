# LateralSight — Prototype LLM+KG pour détection de mouvement latéral

**Résumé**
Prototype démontrant l'extraction d'événements depuis des logs, la construction d'un Knowledge Graph (NetworkX) et une détection basique de scénarios de mouvement latéral.

**Tech stack**
- Python 3.10+
- NetworkX, pandas, scikit-learn, node2vec (ou karateclub), Streamlit
- Optionnel: accès à un LLM via HuggingFace/locale ou API pour extraction NLP

**Structure**
- `data/` : fichiers de logs (CSV / synthetiques)
- `src/extract_events.py` : extraction & normalisation (rules + LLM stub)
- `src/build_graph.py` : construit un graph NetworkX
- `src/detect.py` : règles/matching pour mouvement latéral
- `app.py` : demo Streamlit
- `Dockerfile`, `requirements.txt`

**Quick start**
```bash
git clone https://github.com/TON_COMPTE/LateralSight.git
cd LateralSight
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/extract_events.py data/sample_logs.csv data/events.json
python src/build_graph.py data/events.json data/graph.gml
streamlit run app.py
