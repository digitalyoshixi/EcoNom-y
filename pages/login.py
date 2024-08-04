from utils.database import get_supabase_api
from extra_streamlit_components import CookieManager
import os
import load_env
from database import get_supabase_api
import utils.load_env
import streamlit as st
import sys
import bcrypt
import datetime
import jwt

sys.path.insert(1, "utils")

cookies = CookieManager()
print(cookies.get_all())

supabase_api = get_supabase_api()

st.title("Log into your EcoNom-y account")

form = st.form("my_form")

cookies = CookieManager()


def login():
    username = st.session_state.un
    password = st.session_state.pw

    filtered = True
    if len(username) == 0:
        form.error("Enter your username")
        filtered = False
    if len(password) == 0:
        form.error("Enter your password")
        filtered = False

    if filtered:
        dbpass = supabase_api.selectspecific(
            "profiles", "password", "profile", username)
        if dbpass.count != None:
            hashedpass = dbpass.data[0]["password"]
            match = supabase_api.check_password(password, hashedpass)
            if match:
                jwt_token = supabase_api.create_jwt_token(username)
                token, expiration = jwt_token
                cookies.set("token", token, expires_at=expiration)
                supabase_api.add_token(username, token, expiration)
                st.rerun()  # Reload the page to reflect the login status
            else:
                st.write("Invalid username or password")
        else:
            st.write("Invalid username or password")


with form:
    st.text_input("Username", key="un")
    st.text_input("Password", key="pw", type="password")
    st.form_submit_button("Log in", on_click=login)
