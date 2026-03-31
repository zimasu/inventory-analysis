import pandas as pd
import plotly.express as px
from config import ABC_COLORS, CURRENCY_SYMBOL


def chart_ranked_bar(inventory: pd.DataFrame, top_n: int = 20):
    top_items = inventory.nlargest(top_n, "revenue").sort_values("revenue")

    fig = px.bar(
        top_items,
        x="revenue", y="item_name",
        color="abc_class",
        orientation="h",
        color_discrete_map=ABC_COLORS,
        title=f"Top {top_n} Items by Revenue",
        text="abcxyz_class",
        hover_data=["category", "margin_pct", "abcxyz_class"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title=f"Revenue ({CURRENCY_SYMBOL})",
        yaxis_title="",
        height=600,
        showlegend=True,
    )
    return fig