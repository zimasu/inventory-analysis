import pandas as pd
import plotly.express as px
from config import ABC_COLORS


def chart_treemap(inventory: pd.DataFrame):
    inventory = inventory.copy()
    inventory["abc_class"] = inventory["abc_class"].astype(str)

    fig = px.treemap(
        inventory,
        path=["category", "abc_class", "item_name"],
        values="revenue",
        color="abc_class",
        color_discrete_map=ABC_COLORS,
        title="Revenue Treemap — Category → ABC Class → Item",
        hover_data={"margin_pct": True},
    )
    fig.update_traces(textinfo="label+value+percent root")
    fig.update_layout(height=500)
    return fig