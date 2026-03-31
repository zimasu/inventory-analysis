import pandas as pd
import plotly.express as px
from config import STOCKOUT_THRESHOLD_DAYS


def chart_scatter(inventory: pd.DataFrame):
    fig = px.scatter(
        inventory,
        x="avg_days_in_stock",
        y="margin_pct",
        color="abcxyz_class",
        size="revenue",
        hover_name="item_name",
        hover_data=["category", "units_in_stock", "stockout_days_per_year"],
        title="Days in Stock vs Margin % — sized by Revenue",
        labels={
            "avg_days_in_stock": "Avg Days in Stock",
            "margin_pct": "Margin %",
        },
        size_max=40,
        height=500,
    )

    fig.add_vline(x=STOCKOUT_THRESHOLD_DAYS, line_dash="dash", line_color="gray", annotation_text="Stockout threshold")
    fig.add_hline(y=inventory["margin_pct"].median(), line_dash="dash", line_color="gray", annotation_text="Median margin")

    return fig