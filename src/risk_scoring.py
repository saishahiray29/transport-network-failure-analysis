import pandas as pd


def minmax(series):
    denom = series.max() - series.min()
    if denom == 0:
        return pd.Series(0, index=series.index)
    return (series - series.min()) / denom


def create_risk_scores(df):
    df = df.copy()

    required_cols = [
        "betweenness_centrality",
        "degree_centrality",
        "failure_impact_score",
    ]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["betweenness_norm"] = minmax(df["betweenness_centrality"])
    df["degree_norm"] = minmax(df["degree_centrality"])

    df["propagation_risk_score"] = (
        0.5 * df["betweenness_norm"] +
        0.2 * df["degree_norm"] +
        0.3 * df["failure_impact_score"]
    )

    return df.sort_values("propagation_risk_score", ascending=False)