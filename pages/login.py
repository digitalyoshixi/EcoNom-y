import streamlit as st
from utils.database import SupabaseAPI 

st.title("Log into your EcoNom-y account")

form = st.form('my_form')

def login():
    username = st.session_state.un
    password = st.session_state.pw

    if len(username) == 0:
        form.error("Enter your username")
    if len(password) == 0:
        form.error("Enter your password")


    #communicates with database from here


with form:
    st.text_input("Username", key="un")
    st.text_input("Password", key="pw", type = "password")
    st.form_submit_button("Log in", on_click=login)