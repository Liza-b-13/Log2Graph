import streamlit as st
import src.extract_events as extractor
import src.build_graph as builder
import src.detect as detector
import src.visualize as viz
import src.utils as utils
import networkx as nx
import tempfile, os, json
from time import sleep

st.set_page_config(page_title="LateralSight Demo", layout="wide")

# --- HEADER ---
st.title("🧠 LateralSight — Prototype LLM-assisted Knowledge Graph")
st.markdown("""
Pipeline interactif : **logs → événements → graphe → détection**

💡 **Conseil** : chargez un CSV ou utilisez le fichier d'exemple, puis cliquez sur "🚀 Lancer le pipeline".
""")

st.divider()

# --- USER INPUT ZONE ---
st.subheader("⚙️ Configuration du test")
col1, col2 = st.columns([1,2])
with col1:
    mode = st.radio("Mode d'extraction :", ["rule", "llm"], horizontal=True)
with col2:
    uploaded = st.file_uploader("Importer un fichier CSV (ou utiliser l'exemple fourni)", type=["csv"])

use_sample = False
if uploaded is None:
    st.info("Aucun fichier chargé — le fichier `sample_logs.csv` sera utilisé.")
    use_sample = True

run = st.button("🚀 Lancer le pipeline")

if run:
    # --- Étape 0 : initialisation ---
    progress = st.progress(0)
    status_box = st.empty()

    # Étape 1 : charger le fichier CSV
    status_box.info("📄 Étape 1 — Extraction des événements...")
    sleep(0.3)
    if use_sample:
        csv_path = "sample_logs.csv"
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        tmp.write(uploaded.getvalue())
        tmp.flush()
        csv_path = tmp.name

    events = extractor.parse_csv_to_events(csv_path, mode=mode)
    progress.progress(20)
    status_box.success(f"✅ {len(events)} événements extraits")
    st.json(events[:5])

    # Étape 2 : construire le graphe
    status_box.info("🕸️ Étape 2 — Construction du graphe...")
    sleep(0.3)
    G = builder.build_graph_from_events(events)
    builder.save_graph_gml(G, "tmp_graph.gml")
    progress.progress(50)
    st.success(f"Graphe construit : **{len(G.nodes())} nœuds**, **{len(G.edges())} arêtes**")

    # Étape 3 : détection
    status_box.info("🚨 Étape 3 — Détection d’anomalies...")
    sleep(0.3)
    kb = utils.read_json("data/kb_patterns.json")
    alerts = detector.detect_patterns_in_graph(G, kb)
    progress.progress(75)

    if alerts:
        st.error(f"{len(alerts)} alerte(s) détectée(s) ❗")
        for a in alerts:
            st.markdown(f"**Pattern:** {a['pattern_name']}\n**Chemin:** {a['path']}\n**Actions:** {a['actions_sequence']}")
    else:
        st.success("✅ Aucune alerte détectée")

    # Étape 4 : visualisation
    status_box.info("🔍 Étape 4 — Visualisation du graphe...")
    sleep(0.3)
    fig = viz.draw_graph(G, figsize=(10,7))
    st.pyplot(fig)
    progress.progress(100)
    status_box.success("🎉 Pipeline terminé !")

    if not use_sample:
        os.unlink(csv_path)

# --- SIDEBAR ---
st.sidebar.header("ℹ️ Aide & infos")
st.sidebar.markdown("""
**LateralSight** permet de :
- Extraire des événements à partir de logs
- Construire un graphe de relations
- Détecter des patterns suspects
- Visualiser les interactions

💻 Développé pour illustrer un pipeline *LLM-assisted Knowledge Graph*.
""")
