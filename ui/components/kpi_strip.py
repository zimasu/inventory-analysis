import streamlit as st
from config import CURRENCY_SYMBOL, STOCKOUT_THRESHOLD_DAYS


def render_kpi_strip(inventory):
    items_with_stockouts = inventory[inventory["stockout_days_per_year"] > STOCKOUT_THRESHOLD_DAYS]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Items",    len(inventory))
    col2.metric("Total Revenue",  f"{CURRENCY_SYMBOL} {inventory['revenue'].sum():,.0f}")
    col3.metric("Avg Margin",     f"{inventory['margin_pct'].mean():.1f}%")
    col4.metric("Stockout Items", len(items_with_stockouts))