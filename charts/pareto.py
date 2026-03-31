import pandas as pd
import plotly.graph_objects as go
from config import CURRENCY_SYMBOL


def chart_pareto(inventory: pd.DataFrame, top_n: int = 20):
    top_items = inventory.sort_values("revenue", ascending=False).head(top_n)

    fig = go.Figure()

    fig.add_bar(
        x=top_items["item_name"],
        y=top_items["revenue"],
        name="Revenue",
    )

    fig.add_scatter(
        x=top_items["item_name"],
        y=top_items["cumulative_revenue_pct"],
        name="Cumulative %",
        yaxis="y2",
        line=dict(width=2),
        mode="lines+markers",
    )

    fig.update_layout(
        title=f"Pareto Chart — Top {top_n} Items",
        xaxis_tickangle=-45,
        yaxis=dict(title=f"Revenue ({CURRENCY_SYMBOL})"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 110]),
        legend=dict(x=0.01, y=0.99),
        height=450,
    )

    return fig