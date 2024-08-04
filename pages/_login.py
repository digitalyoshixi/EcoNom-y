import streamlit as st
from utils.database import get_supabase_api
from utils.cookies import CookieManagerAPI

# Load APIS
supabase_api = get_supabase_api()
cookie_manager = CookieManagerAPI()


def showpage():
    def login():
        username = st.session_state.un
        password = st.session_state.pw

        filtered = True
        if len(username) == 0:
            st.session_state.form.error("Enter your username")
            filtered = False
        if len(password) == 0:
            st.session_state.form.error("Enter your password")
            filtered = False

        if filtered:
            dbpass = supabase_api.selectspecific(
                "profiles", "password", "profile", username
            )
            if len(dbpass.data) != 0:
                hashedpass = dbpass.data[0]["password"]
                match = supabase_api.check_password(password, hashedpass)
                if match:
                    jwt_token = supabase_api.create_jwt_token(username)
                    token, expiration = jwt_token
                    cookie_manager.setcookie("token", token, expires_at=expiration)
                    supabase_api.add_token(username, token, str(expiration))
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Invalid username or password")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("my_form") as form:
            st.session_state.form = form
            st.text_input("Username", key="un")
            st.text_input("Password", key="pw", type="password")
            st.form_submit_button("Log in", on_click=login)

        if st.button("Don't have an account? Register one here."):
            st.switch_page("pages/_signup.py")
    else:
        st.write("You are already logged in")


st.title("Log into your EcoNom-y account")

tokenvalidity = cookie_manager.getcookie("token")
if tokenvalidity:
    st.session_state.logged_in = True

showpage()
