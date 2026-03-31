# dashboard.py
import streamlit as st
from utils.analysis_runner import load_and_classify_inventory
from ui.components.briefing import render_briefing            # handles everything on Overview
from ui.components.hero_2x2 import render_hero                # moved to Charts tab
from ui.components.matrix_3x3 import render_matrix
from ui.components.chart_section import render_charts
from ui.components.deep_dive import render_deep_dive
from ui.components.math_proof import render_math_proof


def render_dashboard(config: dict, uploaded_file):
    st.title("📦 Inventory Analysis")

    try:
        inventory, warnings = load_and_classify_inventory(uploaded_file, config)
        for warning in warnings:
            st.warning(warning)
    except ValueError as error:
        st.error(f"❌ {error}")
        st.stop()

    overview, charts, matrix, deep_dive, how_it_works = st.tabs([
        "Overview", "Charts", "Matrix", "Deep Dive", "How it Works",
    ])

    with overview:
        render_briefing(inventory)        # summary + KPI cards + notification feed

    with charts:
        render_hero(inventory)            # bubble chart lives here now
        render_charts(inventory)

    with matrix:
        render_matrix(inventory)

    with deep_dive:
        render_deep_dive(inventory)

    with how_it_works:
        render_math_proof(inventory, config)