import streamlit as st
import os
from utils.database import get_supabase_api
from utils.cookies import get_cookie_manager

supabase_api = get_supabase_api()
cookie_manager = get_cookie_manager()


def show_sidebar():
    user_id = supabase_api.verify_token(cookie_manager.getcookie("token"))
    if user_id:
        st.sidebar.text(f"Logged in as {user_id}.")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    pages_dir = os.path.join(current_dir, "..", "pages")

    st.sidebar.page_link("Home.py", label="Home")

    for page in os.listdir(pages_dir):
        if not page.startswith("_"):
            st.sidebar.page_link(f"pages/{page}", label=page.replace("_", " ")[:-3])
