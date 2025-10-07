# app.py
import streamlit as st
import src.extract_events as extractor
import src.build_graph as builder
import src.detect as detector
import src.visualize as viz
import src.utils as utils
import networkx as nx
import tempfile, os, json

st.set_page_config(page_title="LateralSight demo", layout="wide")

st.title("LateralSight — Prototype LLM-assisted Knowledge Graph")
st.markdown("Pipeline: logs → events → KG → detection (mode: rule / llm-simulated)")

# Sidebar: uploader & options
st.sidebar.header("Options")
mode = st.sidebar.radio("Mode d'extraction", ["llm", "rule"])
uploaded = st.sidebar.file_uploader("Charger un fichier CSV (sample_logs.csv par défaut)", type=["csv"])
use_sample = False
if uploaded is None:
    st.sidebar.write("Aucun fichier uploadé — j'utilise sample_logs.csv de l'exemple.")
    use_sample = True

if st.sidebar.button("Run pipeline"):
    # save uploaded to temp if present
    if use_sample:
        csv_path = "sample_logs.csv"
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        tmp.write(uploaded.getvalue())
        tmp.flush()
        csv_path = tmp.name

    st.info(f"Extraction des événements (mode={mode})...")
    events = extractor.parse_csv_to_events(csv_path, mode=mode)
    st.success(f"{len(events)} événements extraits")
    # show sample events
    st.json(events[:5])

    # build graph
    G = builder.build_graph_from_events(events)
    st.success(f"Graphe construit: {len(G.nodes())} noeuds, {len(G.edges())} arêtes")

    # save graph to temp gml
    gml_tmp = "tmp_graph.gml"
    builder.save_graph_gml(G, gml_tmp)

    # detection
    kb = utils.read_json("data/kb_patterns.json")
    alerts = detector.detect_patterns_in_graph(G, kb)
    if alerts:
        st.error(f"{len(alerts)} alertes détectées")
        for a in alerts:
            st.write(a)
    else:
        st.success("Aucune alerte détectée")

    # visualization
    st.header("Visualisation du graphe")
    fig = viz.draw_graph(G)
    st.pyplot(fig)

    if not use_sample:
        os.unlink(csv_path)
