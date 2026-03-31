import streamlit as st


def render_math_proof(inventory, config: dict):
    st.subheader("🧮 How the Numbers Work")
    st.caption("Step-by-step breakdown of every formula used in this analysis.")

    st.markdown("#### ABC — Revenue Contribution")
    st.markdown(f"""
    1. Sort all items by revenue descending
    2. Compute cumulative revenue share: `cumulative % = cumsum(revenue) / sum(revenue)`
    3. Assign class:
       - **A** — top {int(config['threshold_a'] * 100)}% of cumulative revenue
       - **B** — next {int((config['threshold_b'] - config['threshold_a']) * 100)}% 
       - **C** — remaining items
    """)
    st.dataframe(inventory[["item_code", "item_name", "revenue", "abc_class"]].sort_values("revenue", ascending=False).head(10).reset_index(drop=True), use_container_width=True)

    st.markdown("#### XYZ — Demand Variability")
    st.markdown(f"""
    1. Compute coefficient of variation per item: `CV = std(monthly_sales) / mean(monthly_sales)`
    2. Assign class:
       - **X** — CV ≤ {config['threshold_x']} → stable demand
       - **Y** — CV {config['threshold_x']}–{config['threshold_y']} → variable demand
       - **Z** — CV > {config['threshold_y']} → highly unpredictable
    """)
    st.dataframe(inventory[["item_code", "item_name", "cv", "xyz_class"]].sort_values("cv").head(10).reset_index(drop=True), use_container_width=True)

    st.markdown("#### Combined ABC/XYZ")
    st.markdown("Simply concatenate the two classes: `abcxyz_class = abc_class + xyz_class`. An item that is **A** and **X** becomes **AX** — high revenue, stable demand — your most important item.")
    st.dataframe(inventory[["item_code", "item_name", "abc_class", "xyz_class", "abcxyz_class"]].sort_values(["abc_class", "xyz_class"]).head(10).reset_index(drop=True), use_container_width=True)