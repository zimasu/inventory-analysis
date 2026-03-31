import streamlit as st                                          # web app framework
from config import ABC_DEFAULTS, XYZ_DEFAULTS, SLIDER_BOUNDS   # default values and slider bounds


def render_sidebar() -> dict:
    with st.sidebar:
        st.header("⚙️ Settings")                                # show sidebar title

        st.subheader("ABC — Revenue Contribution")              # ABC threshold section
        threshold_a = st.slider("Class A cutoff (%)", *SLIDER_BOUNDS["abc_a"], int(ABC_DEFAULTS["threshold_a"] * 100)) / 100  # convert % to decimal
        threshold_b = st.slider("Class B cutoff (%)", *SLIDER_BOUNDS["abc_b"], int(ABC_DEFAULTS["threshold_b"] * 100)) / 100  # convert % to decimal

        st.subheader("XYZ — Demand Variability")                # XYZ threshold section
        threshold_x = st.slider("Class X cutoff (CV)", *SLIDER_BOUNDS["xyz_x"], XYZ_DEFAULTS["threshold_x"])  # coefficient of variation
        threshold_y = st.slider("Class Y cutoff (CV)", *SLIDER_BOUNDS["xyz_y"], XYZ_DEFAULTS["threshold_y"])  # coefficient of variation

        st.divider()
        if st.button("📂 Upload a different file"):             # clear file and return to upload screen
            st.session_state.uploaded_file = None
            st.rerun()

    return {                                                    # return chosen thresholds to dashboard
        "threshold_a": threshold_a,
        "threshold_b": threshold_b,
        "threshold_x": threshold_x,
        "threshold_y": threshold_y,
    }