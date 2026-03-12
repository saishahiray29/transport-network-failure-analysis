import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# --------------------------------------------------
# Page settings
# --------------------------------------------------
st.set_page_config(
    page_title="London Underground Failure Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.network_utils import build_graph, simulate_station_failure, get_network_stats

PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# Check required files
# --------------------------------------------------
required_files = [
    PROCESSED_DIR / "stations_clean.csv",
    PROCESSED_DIR / "connections_clean.csv",
    PROCESSED_DIR / "station_metrics.csv",
    PROCESSED_DIR / "failure_results.csv",
    PROCESSED_DIR / "top_station_risk_scores.csv",
]

missing_files = [str(f.name) for f in required_files if not f.exists()]
if missing_files:
    st.error(f"Missing required files: {missing_files}")
    st.stop()

# --------------------------------------------------
# Load data
# --------------------------------------------------
@st.cache_data
def load_data(processed_dir):
    stations = pd.read_csv(processed_dir / "stations_clean.csv")
    connections = pd.read_csv(processed_dir / "connections_clean.csv")
    metrics = pd.read_csv(processed_dir / "station_metrics.csv")
    failure_results = pd.read_csv(processed_dir / "failure_results.csv")
    risk_scores = pd.read_csv(processed_dir / "top_station_risk_scores.csv")
    return stations, connections, metrics, failure_results, risk_scores


@st.cache_resource
def load_graph(stations, connections):
    return build_graph(stations, connections)


stations, connections, metrics, failure_results, risk_scores = load_data(PROCESSED_DIR)
G = load_graph(stations, connections)
baseline_stats = get_network_stats(G)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("London Underground Failure Propagation Dashboard")
st.caption(
    "This dashboard uses graph network analysis and failure simulation to identify London Underground stations that have the greatest impact on connectivity, travel efficiency and disruption propagation."
)

# --------------------------------------------------
# Top KPI cards
# --------------------------------------------------
k1, k2, k3 = st.columns(3)
k1.metric("Stations in Main Network", G.number_of_nodes())
k2.metric("Connections in Main Network", G.number_of_edges())
k3.metric("Baseline Avg Shortest Path", round(baseline_stats["avg_shortest_path"], 2))

st.divider()

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["Top Risk Stations", "Failure Simulation", "Failure Impact"]
)

# ==================================================
# TAB 1 — TOP RISK STATIONS
# ==================================================
with tab1:
    st.subheader("Top Critical Stations by Propagation Risk Score")

    top10 = (
        risk_scores.sort_values("propagation_risk_score", ascending=False)
        .head(10)
        .copy()
    )

    top10["propagation_risk_score"] = top10["propagation_risk_score"].round(3)
    top10["failure_impact_score"] = top10["failure_impact_score"].round(3)
    top10["betweenness_centrality"] = top10["betweenness_centrality"].round(3)

    left_col, right_col = st.columns([1.05, 1.35])

    with left_col:
        display_top10 = top10[
            [
                "station_display",
                "propagation_risk_score",
                "failure_impact_score",
                "betweenness_centrality"
            ]
        ].rename(
            columns={
                "station_display": "Station",
                "propagation_risk_score": "Propagation Risk",
                "failure_impact_score": "Failure Impact",
                "betweenness_centrality": "Betweenness",
            }
        )

        st.dataframe(display_top10, use_container_width=True)
        st.caption(
            "This ranking combines centrality and simulated disruption impact to identify structurally important stations."
        )

    with right_col:
        fig = px.bar(
            top10,
            x="station_display",
            y="propagation_risk_score",
            color="propagation_risk_score",
            title="Top 10 Stations by Propagation Risk Score"
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Risk Score",
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TAB 2 — FAILURE SIMULATION
# ==================================================
with tab2:
    st.subheader("Simulate a Station Failure")

    station_choice = st.selectbox(
        "Choose a station",
        sorted(G.nodes())
    )

    if st.button("Run Simulation"):
        failed_graph = simulate_station_failure(G, station_choice)
        failed_stats = get_network_stats(failed_graph)

        c1, c2, c3 = st.columns(3)
        c1.metric("Baseline Components", baseline_stats["num_components"])
        c2.metric("Baseline Largest Component", baseline_stats["largest_component_size"])
        c3.metric("Baseline Avg Shortest Path", round(baseline_stats["avg_shortest_path"], 2))

        c4, c5, c6 = st.columns(3)
        c4.metric("After Failure Components", failed_stats["num_components"])
        c5.metric("After Failure Largest Component", failed_stats["largest_component_size"])
        c6.metric("After Failure Avg Shortest Path", round(failed_stats["avg_shortest_path"], 2))

        if failed_stats["num_components"] > baseline_stats["num_components"]:
            st.warning("This station failure fragments the network into multiple components.")
        elif failed_stats["avg_shortest_path"] > baseline_stats["avg_shortest_path"]:
            st.info("This station failure increases travel distance without breaking the network apart.")
        else:
            st.success("This station has relatively low structural impact on the network.")

        impact_df = failure_results[
            failure_results["station_removed"] == station_choice
        ].copy()

        if not impact_df.empty:
            impact_df["avg_shortest_path"] = impact_df["avg_shortest_path"].round(2)
            impact_df["failure_impact_score"] = impact_df["failure_impact_score"].round(3)

            display_impact = impact_df[
                [
                    "station_display",
                    "num_components",
                    "largest_component_size",
                    "avg_shortest_path",
                    "failure_impact_score"
                ]
            ].rename(
                columns={
                    "station_display": "Station",
                    "num_components": "Components",
                    "largest_component_size": "Largest Component",
                    "avg_shortest_path": "Avg Shortest Path",
                    "failure_impact_score": "Failure Impact",
                }
            )

            st.subheader("Stored Failure Metrics")
            st.dataframe(display_impact, use_container_width=True)

# ==================================================
# TAB 3 — FAILURE IMPACT
# ==================================================
with tab3:
    st.subheader("Top Stations by Failure Impact Score")

    top_failure = (
        failure_results.sort_values("failure_impact_score", ascending=False)
        .head(10)
        .copy()
    )

    top_failure["failure_impact_score"] = top_failure["failure_impact_score"].round(3)

    left_col, right_col = st.columns([1.05, 1.35])

    with left_col:
        failure_table = top_failure[
            [
                "station_display",
                "failure_impact_score",
                "num_components",
                "largest_component_size"
            ]
        ].rename(
            columns={
                "station_display": "Station",
                "failure_impact_score": "Failure Impact",
                "num_components": "Components",
                "largest_component_size": "Largest Component",
            }
        )

        st.dataframe(failure_table, use_container_width=True)
        st.caption(
            "Higher scores indicate stations whose removal causes greater structural disruption."
        )

    with right_col:
        fig2 = px.bar(
            top_failure,
            x="station_display",
            y="failure_impact_score",
            color="failure_impact_score",
            title="Top 10 Stations by Failure Impact Score"
        )
        fig2.update_layout(
            xaxis_title="",
            yaxis_title="Failure Impact Score",
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)