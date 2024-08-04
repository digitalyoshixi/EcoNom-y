import streamlit as st
from utils.cookies import get_cookie_manager
from utils.database import get_supabase_api

supabase_api = get_supabase_api()
cookie_manager = get_cookie_manager()


def redirect_to_login():
    st.write("You are not logged in. Redirecting to login page...")
    st.switch_page("pages/_login.py")

def redirect_to_home():
    st.write("You are logged in. Redirecting to home page...")
    st.switch_page("Home.py")

def redirect_to_pt():
    st.write("You are logged in. Redirecting to portion tracker page...")
    st.switch_page("Portion_Tracker.py")

def is_logged_in() -> str:
    token = cookie_manager.getcookie("token")
    if not token:
        return False

    user_id = supabase_api.verify_token(token)
    if not user_id:
        return False

    return user_id


def require_auth():
    if not is_logged_in():
        redirect_to_login()


def require_non_auth():
    if is_logged_in():
        redirect_to_home()
