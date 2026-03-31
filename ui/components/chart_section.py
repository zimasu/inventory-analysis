import streamlit as st                                          # web app framework
from charts.treemap import chart_treemap                        # revenue treemap
from charts.bar import chart_ranked_bar                         # top items bar chart
from charts.scatter import chart_scatter                        # days in stock vs margin
from charts.pareto import chart_pareto                          # pareto curve
from config import PLOTLY_CONFIG, PLOTLY_USE_CONTAINER_WIDTH     # shared chart display settings                           # stretch charts to full container width

def render_charts(inventory):
    treemap, bar, scatter, pareto = st.tabs([                   # create chart navigation tabs
        "Treemap", "Top Items", "Stock vs Margin", "Pareto",
    ])

    with treemap:                                               # revenue by category and ABC class
        st.plotly_chart(chart_treemap(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)

    with bar:                                                   # top 20 items by revenue
        st.plotly_chart(chart_ranked_bar(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)

    with scatter:                                               # days in stock vs margin bubble chart
        st.plotly_chart(chart_scatter(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)

    with pareto:                                                # cumulative revenue curve
        st.plotly_chart(chart_pareto(inventory), use_container_width=PLOTLY_USE_CONTAINER_WIDTH, config=PLOTLY_CONFIG)