import io                                                       # converts raw bytes back into a readable file
import streamlit as st                                          # web app framework
from utils.data_loader import load_csv                          # reads and validates the CSV
from analysis.combined import calculate_abcxyz                  # runs ABC and XYZ classification

@st.cache_data                                                  # skip reprocessing if nothing changed
def load_and_classify_inventory(file_bytes: bytes, config: dict):
    file = io.BytesIO(file_bytes)                               # wrap bytes so pandas can read it
    inventory, warnings = load_csv(file)                        # read and validate CSV
    classified_inventory = calculate_abcxyz(inventory, **config) # classify each item A/B/C and X/Y/Z
    return classified_inventory, warnings                       # return inventory and any warnings