import streamlit as st                                          # web app framework
from config import PAGE_CONFIG                                  # app title, icon, layout settings
from ui.upload_screen import render_upload_screen               # upload screen before file is picked
from ui.sidebar import render_sidebar                           # settings panel on the left
from ui.dashboard import render_dashboard                       # main analysis screen

st.set_page_config(**PAGE_CONFIG)                               # set browser tab title and layout

st.markdown("""
    <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="stDecoration"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# hide anchor links on all headings
st.markdown("""
    <style>
    .stMarkdown a[href^="#"] { display: none; }
    [data-testid="stMarkdownContainer"] a { display: none; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.get("uploaded_file"):                   # no file uploaded yet
    st.session_state.uploaded_file = render_upload_screen()     # show upload screen, save file when picked
else:
    config = render_sidebar()                                   # collect threshold settings
    render_dashboard(config, st.session_state.uploaded_file)    # show full analysis