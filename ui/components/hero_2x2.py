import streamlit as st                                          # web app framework
from charts.hero import chart_hero_2x2                         # 2x2 inventory health bubble chart
from config import PLOTLY_CONFIG, PLOTLY_USE_CONTAINER_WIDTH    # shared chart display settings


def render_hero(inventory):
    st.subheader("🗺️ Inventory Health — At a Glance")          # show section title
    st.caption("Each bubble is one item. Size = revenue. Click legend to filter.")
    st.plotly_chart(chart_hero_2x2(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)  # render chart