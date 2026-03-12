# London Underground Failure Propagation Dashboard

This project models the London Underground as a graph network to identify structurally critical stations, simulate station failures, and measure how disruptions propagate through the system.

The project combines network analysis, failure simulation, and operational performance data to study resilience in a real-world transport network.  
An interactive Streamlit dashboard allows users to explore critical stations, simulate failures, and compare network behaviour before and after disruptions.


---

## Project Overview

Transport networks are highly interconnected systems where failures at key locations can cause widespread disruption.  
In this project, the London Underground is represented as a graph where:

- Nodes = stations  
- Edges = connections between stations  

The network is analysed using graph theory to find stations that are most important for:

- Connectivity
- Network resilience
- Travel efficiency
- Delay propagation
- Disruption impact

The final results are shown in an interactive Streamlit dashboard.


---

## Features

- Build Underground network graph from TfL data
- Compute centrality metrics
- Simulate failure of each station
- Measure network fragmentation
- Measure change in shortest path length
- Create failure impact score
- Create propagation risk score
- Interactive Streamlit dashboard with tabs
- KPI comparison before / after failure


---

## Data Sources

The project uses real transport data:

- TfL StopPoint API (station data)
- TfL Line Route API (connections)
- service-operated.csv
- kilometres-operated.csv
- excess-journey-time.csv
- orr_station_usage.csv
- trains_planned.csv


---

## Workflow

The project is built using a notebook-based workflow.

1. data_collection.ipynb  
2. data_cleaning.ipynb  
3. network_building.ipynb  
4. network_metrics.ipynb  
5. failure_simulation.ipynb  
6. performance_analysis.ipynb  
7. propagation_delay.ipynb  
8. visuals.ipynb  


---

## Methodology

### 1. Data Collection

Station and route data are collected from the TfL API.

Outputs:
data/processed/tfl_stations.csv
data/processed/tube_connections.csv


Performance datasets are loaded from CSV files.


---

### 2. Data Cleaning

Station names are standardised so that nodes and edges match correctly.

Outputs:

Performance datasets are loaded from CSV files.


---

### 2. Data Cleaning

Station names are standardised so that nodes and edges match correctly.

Outputs:
data/processed/stations_clean.csv
data/processed/connections_clean.csv


---

### 3. Network Building

The Underground network is converted into a graph using NetworkX.

- Nodes = stations
- Edges = connections

Only the largest connected component is used for analysis.


---

### 4. Network Metrics

We compute:

- Degree centrality
- Betweenness centrality
- Closeness centrality

Output:
data/processed/station_metrics.csv


---

### 5. Failure Simulation

Each station is removed from the graph and the network is re-analysed.

We measure:

- number of connected components
- largest component size
- average shortest path

Failure impact score:
failure_impact_score =
0.4 * components_norm + 0.3 * largest_component_loss_norm + 0.3 * avg_shortest_path_norm


Output:
data/processed/failure_results.csv


---

### 6. Propagation Risk Score

Centrality and failure impact are combined.
propagation_risk_score =
0.5 * betweenness_norm + 0.2 * degree_norm + 0.3 * components_norm


Output:
data/processed/top_station_risk_scores.csv



---

### 7. Dashboard

The Streamlit dashboard shows:

- Top risk stations
- Failure simulation
- Network comparison
- Failure impact ranking
- KPI cards
- Tab navigation

Run with:
streamlit run dashboard/app.py



---

## Project Structure

transport-network-failure-analysis/

data/
raw/
processed/

notebooks/
data_collection.ipynb
data_cleaning.ipynb
network_building.ipynb
network_metrics.ipynb
failure_simulation.ipynb
performance_analysis.ipynb
propagation_delay.ipynb
visuals.ipynb

src/
network_utils.py
risk_scoring.py

dashboard/
app.py

outputs/

requirements.txt
README.md
.gitignore


---

## Installation

Clone repository
git clone https://github.com/saishahiray29/transport-network-failure-analysis.git

cd transport-network-failure-analysis

Create virtual environment:
python -m venv venv
venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Run dashboard:
streamlit run dashboard/app.py



---

## Key Insights

- A small number of stations have very high propagation risk.
- Central stations increase travel distance when removed.
- Some failures fragment the network into multiple components.
- Combining centrality and simulation gives better results than using one metric alone.


---

## Author

Saisha Prashant Hiray 

GitHub: https://github.com/saishahiray29  
LinkedIn: https://linkedin.com/in/saisha-hiray 


---

## License

This project is for educational and portfolio use.

=======
# transport-network-failure-analysis
Graph based analysis of the London Underground network to identify structurally critical stations, simulate failures, and measure disruption propagation using NetworkX, performance datasets, and an interactive Streamlit dashboard for resilience and risk analysis.
>>>>>>> bec9d887d97f70d67025de3a8b333127945fb91f
