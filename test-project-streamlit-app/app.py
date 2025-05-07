# File: app.py
import streamlit as st
import os

# Set page config must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Country Currency Database", page_icon="🌎")

from src.database import DatabaseManager
from src.ui import CountryCurrencyUI
from src.utils import load_css

def main():
    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    st.markdown(load_css(css_path), unsafe_allow_html=True)
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create and render UI
    ui = CountryCurrencyUI(db_manager)
    ui.render()

if __name__ == "__main__":
    main()