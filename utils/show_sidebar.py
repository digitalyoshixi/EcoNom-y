import streamlit as st
import os


def show_sidebar():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    pages_dir = os.path.join(current_dir, "..", "pages")

    st.sidebar.page_link("Home.py", label="Home")

    for page in os.listdir(pages_dir):
        if not page.startswith("_"):
            st.sidebar.page_link(f"pages/{page}", label=page.replace("_", " ")[:-3])
