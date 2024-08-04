from extra_streamlit_components import CookieManager
import os
import load_env
from database import get_supabase_api
import streamlit as st
import sys
import bcrypt
import datetime
import jwt

sys.path.insert(1, "utils")

cookies = CookieManager()
print(cookies.get_all())

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
supabase_api = get_supabase_api()

st.title("Log into your EcoNom-y account")

form = st.form("my_form")


def create_jwt_token(user_id):
    expiration = str(datetime.datetime.utcnow() + datetime.timedelta(hours=1))
    payload = {"user_id": user_id, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token, expiration


def login():
    username = st.session_state.un
    password = st.session_state.pw

    filtered = True
    # Filters
    if len(username) == 0:
        form.error("Enter your username")
        filtered = False
    if len(password) == 0:
        form.error("Enter your password")
        filtered = False

    # communicates with database from here
    if filtered:
        dbpass = supabase_api.selectspecific(
            "profiles", "password", "profile", username
        )
        print(dbpass)
        if dbpass.count != None:
            hashedpass = dbpass.data[0][
                "password"
            ]  # get the hashed password in string form
            # If the passwords match
            match = bcrypt.checkpw(
                bytes(password, "utf-8"), bytes(hashedpass, "utf-8")
            )  # see if inputted psasword is same as the hased password in database
            # make a session cookie
            jwt_token = create_jwt_token(username)
            token = jwt_token[0]
            expiration = jwt_token[1]
            # st.session_state.token = token
            cookies = CookieManager()
            cookies.set("token", 12)
            print(cookies.get_all())
            supabase_api.add_token(username, token, expiration)
        else:
            st.write("Username or password not in database")


with form:
    st.text_input("Username", key="un")
    st.text_input("Password", key="pw", type="password")
    st.form_submit_button("Log in", on_click=login)
