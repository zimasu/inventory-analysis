import pandas as pd
import plotly.graph_objects as go


def chart_abcxyz_heatmap(inventory: pd.DataFrame):
    counts = (
        inventory.groupby(["abc_class", "xyz_class"])["item_code"]
        .count()
        .reset_index()
    )
    counts.columns = ["abc_class", "xyz_class", "item_count"]

    pivot = (
        counts
        .pivot(index="abc_class", columns="xyz_class", values="item_count")
        .reindex(index=["A", "B", "C"], columns=["X", "Y", "Z"])
        .fillna(0)
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=["X — Stable", "Y — Variable", "Z — Irregular"],
        y=["A — High value", "B — Mid value", "C — Low value"],
        colorscale="RdYlGn",
        reversescale=True,
        text=pivot.values,
        texttemplate="%{text:.0f} items",
        showscale=True,
        hoverongaps=False,
    ))

    fig.update_layout(
        title="ABC / XYZ Classification Matrix",
        xaxis_title="Demand Predictability →",
        yaxis_title="← Revenue Contribution",
        height=380,
    )

    return fig