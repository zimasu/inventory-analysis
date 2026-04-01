import streamlit as st
from datetime import datetime
from ui.components.briefing import render_briefing
from ui.components.hero_2x2 import render_hero


def render_dashboard(config: dict, inventory):
    st.title("📦 Inventory Analysis")

    overview, about = st.tabs(["Overview", "📋 About this Report"])

    with overview:
        render_hero(inventory)
        render_briefing(inventory)

    with about:
        st.markdown("### How this report works")
        st.markdown(
            """
            This dashboard analyses your inventory automatically every time it loads — 
            no manual uploads needed.

            **ABC Analysis** ranks your products by revenue contribution:
            - 🟢 **A items** — top 70% of revenue. Highest priority.
            - 🟡 **B items** — next 20%. Monitor regularly.
            - 🔴 **C items** — bottom 10%. Review for discontinuation.

            **XYZ Analysis** measures how predictable demand is:
            - **X** — stable, easy to forecast
            - **Y** — some variability, manageable
            - **Z** — irregular, hard to predict

            Combined, **ABC/XYZ** tells you both *what matters* and *how reliably it sells*.
            """
        )
        st.divider()
        st.caption(f"Data last refreshed: {datetime.now().strftime('%d %B %Y, %H:%M')}")
