import streamlit as st
from config import PAGE_CONFIG
from ui.components.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from data.extractor import (
    fetch_product_ids,
    fetch_product_details,
    fetch_stock,
    fetch_sales,
    save_to_csv,
    save_sales_history_to_csv,
)
from config import INVENTORY_FILE, SALES_FILE
from services.analysis_service import run_analysis


st.set_page_config(**PAGE_CONFIG)

st.markdown(
    """
    <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="stDecoration"] {display: none !important;}
        .stMarkdown a[href^="#"] { display: none; }
        [data-testid="stMarkdownContainer"] a { display: none; }
    </style>
""",
    unsafe_allow_html=True,
)


def fetch_from_prestashop():
    progress = st.status("Connecting to your store...", expanded=False)
    with progress:
        st.write("📦 Loading product list...")
        ids = fetch_product_ids()

        st.write(f"🔍 Reading {len(ids)} products...")
        products = fetch_product_details(ids)

        st.write("🏷️ Checking stock levels...")
        products = fetch_stock(products)

        st.write("📊 Pulling sales history...")
        products, sales_by_month = fetch_sales(products)

        st.write("💾 Preparing your report...")
        save_to_csv(products, INVENTORY_FILE)
        save_sales_history_to_csv(sales_by_month, SALES_FILE)

        progress.update(label="Store data ready ✅", state="complete")


fetch_from_prestashop()

config = render_sidebar()

try:
    inventory, warnings = run_analysis(config)
    for w in warnings:
        st.warning(w)
    render_dashboard(config, inventory)
except Exception as e:
    st.error(f"Something went wrong loading the analysis. Please refresh the page.")
    st.exception(e)
