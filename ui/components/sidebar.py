import streamlit as st
from config import ABC_DEFAULTS, XYZ_DEFAULTS, SLIDER_BOUNDS


def render_sidebar() -> dict:
    with st.sidebar:
        st.header("⚙️ Settings")

        st.subheader("ABC — Revenue Contribution")
        threshold_a = (
            st.slider(
                "Class A cutoff (%)",
                *SLIDER_BOUNDS["abc_a"],
                int(ABC_DEFAULTS["threshold_a"] * 100)
            )
            / 100
        )
        threshold_b = (
            st.slider(
                "Class B cutoff (%)",
                *SLIDER_BOUNDS["abc_b"],
                int(ABC_DEFAULTS["threshold_b"] * 100)
            )
            / 100
        )

        st.subheader("XYZ — Demand Variability")
        threshold_x = st.slider(
            "Class X cutoff (CV)", *SLIDER_BOUNDS["xyz_x"], XYZ_DEFAULTS["threshold_x"]
        )
        threshold_y = st.slider(
            "Class Y cutoff (CV)", *SLIDER_BOUNDS["xyz_y"], XYZ_DEFAULTS["threshold_y"]
        )

    return {
        "threshold_a": threshold_a,
        "threshold_b": threshold_b,
        "threshold_x": threshold_x,
        "threshold_y": threshold_y,
    }
