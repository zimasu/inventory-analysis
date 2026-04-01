import streamlit as st                                          # web app framework


def render_upload_screen():
    left_gap, main_content, right_gap = st.columns([1, 2, 1])  # center content on page
    with main_content:
        st.title("📦 Know Your Inventory")                      # outcome focused title
        st.caption("Upload your inventory CSV and instantly see which items make money, which are risky, and which to cut.")  # benefit focused CTA
        st.divider()
        uploaded_file = st.file_uploader("Upload CSV", type="csv", label_visibility="collapsed")  # clean file picker
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file.read()  # store raw bytes not file object
            st.rerun()                                          # move to dashboard immediately
        st.divider()
        with st.expander("What does this app actually do?"):    # FAQ hidden until clicked
            st.write("""
                This app takes your inventory data and automatically sorts every item into one of 9 categories based on two things:
                
                **How much money does it make?** (ABC)
                - A = top 70% of your revenue — your most valuable items
                - B = next 20% — solid performers
                - C = bottom 10% — low contributors
                
                **How predictable is the demand?** (XYZ)
                - X = stable, easy to forecast
                - Y = variable, needs watching
                - Z = unpredictable, hard to plan for
                
                Combine them and you get a clear action plan — AX items get priority stock, CZ items get reviewed for discontinuation.
            """)