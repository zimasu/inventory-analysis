import streamlit as st                                          # web app framework
from charts.matrix import chart_abcxyz_heatmap                 # 3x3 ABC/XYZ heatmap
from config import PLOTLY_CONFIG, PLOTLY_USE_CONTAINER_WIDTH    # shared chart display settings


def render_matrix(inventory):
    st.subheader("🔲 ABC / XYZ Classification Matrix")          # show section title
    st.caption("How many items fall into each of the 9 combinations.")
    st.plotly_chart(chart_abcxyz_heatmap(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)  # render chart