# app.py
import streamlit as st
import src.extract_events as extractor
import src.build_graph as builder
import src.detect as detector
import src.utils as utils
import networkx as nx
import tempfile, os, json
from pyvis.network import Network
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
col1, col2, col3 = st.columns([1,2,1])
with col1:
    mode = st.radio("Mode d'extraction :", ["rule", "llm"], horizontal=True)
with col2:
    uploaded = st.file_uploader("Importer un fichier CSV (ou utiliser l'exemple fourni)", type=["csv"])
with col3:
    user_filter = st.text_input("Filtrer par utilisateur (laisser vide = tous)", "")

use_sample = False
if uploaded is None:
    st.info("Aucun fichier chargé — le fichier `sample_logs.csv` sera utilisé.")
    use_sample = True

run = st.button("🚀 Lancer le pipeline")

if run:
    progress = st.progress(0)
    status_box = st.empty()

    # --- Étape 1 : Extraction
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
    if user_filter:
        events = [e for e in events if e["user"] == user_filter]
    progress.progress(20)
    status_box.success(f"✅ {len(events)} événements extraits")
    st.json(events[:5])

    # --- Étape 2 : Construction du graphe
    status_box.info("🕸️ Étape 2 — Construction du graphe...")
    sleep(0.3)
    G = builder.build_graph_from_events(events)
    builder.save_graph_gml(G, "tmp_graph.gml")
    progress.progress(50)
    st.success(f"Graphe construit : **{len(G.nodes())} nœuds**, **{len(G.edges())} arêtes**")

    # --- Étape 3 : Détection
    status_box.info("🚨 Étape 3 — Détection d’anomalies...")
    sleep(0.3)
    kb = utils.read_json("data/kb_patterns.json")
    alerts = detector.detect_patterns_in_graph(G, kb)
    progress.progress(75)

    if alerts:
        st.error(f"{len(alerts)} alerte(s) détectée(s) ❗")
        for a in alerts:
            st.markdown(
                f"**Pattern:** {a['pattern_name']}\n"
                f"**Chemin:** {a['path']}\n"
                f"**Actions:** {a['actions_sequence']}"
            )
    else:
        st.success("✅ Aucune alerte détectée")

    # --- Étape 4 : Visualisation interactive avec PyVis
    status_box.info("🔍 Étape 4 — Visualisation interactive du graphe...")
    sleep(0.3)

    net = Network(height="600px", width="100%", directed=True)
    color_map = {
        "login": "green",
        "login_failed": "orange",
        "ssh_connect": "blue",
        "privilege_escalation": "red",
        "file_access": "purple",
        "credential_use": "pink",
        "unknown": "gray"
    }

    # Ajouter les noeuds
    for node in G.nodes():
        net.add_node(node, label=node.replace("host:", ""), color="lightgray")

    # Ajouter les arêtes
    for u, v, data in G.edges(data=True):
        actions = [ev["action"] for ev in data.get("events", [])]
        color = color_map.get(actions[-1], "black") if actions else "black"
        title = "<br>".join([f"{ev['action']} ({ev['user']})" for ev in data.get("events", [])])
        net.add_edge(u, v, title=title, color=color)

    net.repulsion(node_distance=200, central_gravity=0.3, spring_length=200)
    net.save_graph("temp_graph.html")
    st.components.v1.html(open("temp_graph.html", "r", encoding="utf-8").read(), height=650)
    
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
- Visualiser les interactions de manière interactive

💻 Développé pour illustrer un pipeline *LLM-assisted Knowledge Graph*.
""")
