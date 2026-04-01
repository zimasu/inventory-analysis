import streamlit as st
from config import PAGE_CONFIG, INVENTORY_FILE, SALES_FILE
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
from services.analysis_service import run_analysis

# Apply execution parameters immediately
st.set_page_config(**PAGE_CONFIG)

# Inject micro-styled presentation overrides cleanly
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

@st.cache_data(show_spinner=False)
def execute_store_synchronization() -> None:
    """
    Ingests and maps database records from PrestaShop REST endpoints securely.
    Cached explicitly to prevent pipeline bottleneck loops on UI re-renders.
    """
    progress = st.status("Connecting to your store store endpoints...", expanded=False)
    with progress:
        st.write("📦 Loading core product schema array...")
        ids = fetch_product_ids()

        st.write(f"🔍 Compiling extraction records for {len(ids)} products...")
        products = fetch_product_details(ids)

        st.write("🏷️ Extracting warehouse metrics and stock counts...")
        products = fetch_stock(products)

        st.write("📊 Restructuring global transactional histories...")
        products, sales_by_month = fetch_sales(products)

        st.write("💾 Serializing runtime files safely to localized storage nodes...")
        save_to_csv(products, INVENTORY_FILE)
        save_sales_history_to_csv(sales_by_month, SALES_FILE)

        progress.update(label="Store pipeline synchronized successfully ✅", state="complete")


# Trigger calculation flow safely inside cached storage memory blocks
execute_store_synchronization()

# Render operational UI workflows
config = render_sidebar()

try:
    inventory, warnings = run_analysis(config)
    for warning in warnings:
        st.warning(warning)
    render_dashboard(config, inventory)
except Exception as runtime_error:
    st.error("Fatal exception trace identified during execution pipeline compilation.")
    st.exception(runtime_error)
