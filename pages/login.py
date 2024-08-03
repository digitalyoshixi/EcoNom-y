import streamlit as st
from utils.database import SupabaseAPI 
from database import get_supabase_api
supabase_api = get_supabase_api()

st.title("Log into your EcoNom-y account")

form = st.form('my_form')

def login():
    username = st.session_state.un
    password = st.session_state.pw

    filtered=True
    # Filters
    if len(username) == 0:
        form.error("Enter your username")
        filtered=False
    if len(password) == 0:
        form.error("Enter your password")
        filtered=False

    #communicates with database from here
    if filtered:
        supabase_api.

with form:
    st.text_input("Username", key="un")
    st.text_input("Password", key="pw", type = "password")
    st.form_submit_button("Log in", on_click=login)