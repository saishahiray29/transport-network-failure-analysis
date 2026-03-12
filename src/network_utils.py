import networkx as nx


def build_graph(stations_df, connections_df):
    used_station_names = set(connections_df["from_name"]).union(set(connections_df["to_name"]))
    stations_df = stations_df[stations_df["station_name"].isin(used_station_names)].copy()

    G = nx.Graph()

    for _, row in stations_df.iterrows():
        G.add_node(
            row["station_name"],
            station_id=row.get("station_id"),
            lat=row.get("lat"),
            lon=row.get("lon")
        )

    for _, row in connections_df.iterrows():
        G.add_edge(
            row["from_name"],
            row["to_name"],
            line=row.get("line")
        )

    if G.number_of_nodes() > 0:
        largest_component = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_component).copy()

    return G


def simulate_station_failure(graph, station_name):
    G_failed = graph.copy()
    if station_name in G_failed:
        G_failed.remove_node(station_name)
    return G_failed


def get_network_stats(graph):
    if graph.number_of_nodes() == 0:
        return {
            "num_components": 0,
            "largest_component_size": 0,
            "avg_shortest_path": None
        }

    components = list(nx.connected_components(graph))
    num_components = len(components)
    largest_component = max(components, key=len)
    largest_subgraph = graph.subgraph(largest_component)

    if largest_subgraph.number_of_nodes() > 1:
        avg_shortest = nx.average_shortest_path_length(largest_subgraph)
    else:
        avg_shortest = None

    return {
        "num_components": num_components,
        "largest_component_size": len(largest_component),
        "avg_shortest_path": avg_shortest
    }