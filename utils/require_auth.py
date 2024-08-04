import streamlit as st
from utils.cookies import CookieManagerAPI
from utils.database import get_supabase_api

supabase_api = get_supabase_api()
cookie_manager = CookieManagerAPI()


def redirect_to_login():
    st.write("You are not logged in. Redirecting to login page...")
    st.switch_page("pages/_login.py")


token = cookie_manager.getcookie("token")
if token:
    user_id = supabase_api.verify_token(token)
    if not user_id:
        redirect_to_login()
    else:
        st.write(f"Logged in as {user_id}")
else:
    redirect_to_login()
