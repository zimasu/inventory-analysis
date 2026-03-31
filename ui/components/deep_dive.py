import streamlit as st
from config import TABLE_COLUMNS, EXPORT_FILENAME


def render_deep_dive(inventory):
    col1, col2 = st.columns(2)
    with col1:
        abc_filter = st.multiselect("Filter by ABC class", ["A", "B", "C"], default=["A", "B", "C"])
    with col2:
        xyz_filter = st.multiselect("Filter by XYZ class", ["X", "Y", "Z"], default=["X", "Y", "Z"])

    filtered_inventory = inventory[
        inventory["abc_class"].isin(abc_filter) &
        inventory["xyz_class"].isin(xyz_filter)
    ]

    with st.expander("📋 Full Item Classification Table"):
        st.dataframe(filtered_inventory[TABLE_COLUMNS].reset_index(drop=True), use_container_width=True)

    with st.expander("📊 Summary Statistics"):
        st.dataframe(filtered_inventory[TABLE_COLUMNS].describe().round(2), use_container_width=True)

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=filtered_inventory.to_csv(index=False).encode("utf-8"),
        file_name=EXPORT_FILENAME,
        mime="text/csv",
    )