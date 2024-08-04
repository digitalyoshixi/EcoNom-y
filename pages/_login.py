import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
from utils.database import get_supabase_api
from utils.cookies import get_cookie_manager, update_cookie_manager
from utils.auth import require_non_auth, is_logged_in

require_non_auth()

# Load APIS
supabase_api = get_supabase_api()
cookie_manager = get_cookie_manager()

st.title("Log into your EcoNom-y account")
form = st.form("my_form")


def login():
    username = st.session_state.username.strip()
    password = st.session_state.password

    try:
        if len(username) == 0:
            raise Exception("Enter your username.")

        elif len(password) == 0:
            raise Exception("Enter your password")

        dbpass = supabase_api.selectspecific(
            "profiles", "password", "username", username
        )

        if len(dbpass.data) == 0:
            raise Exception("Invalid username or password")

        hashedpass = dbpass.data[0]["password"]
        if not supabase_api.check_password(password, hashedpass):
            raise Exception("Invalid username or password")

        jwt_token = supabase_api.create_jwt_token(username)
        token, expiration = jwt_token
        cookie_manager.setcookie("token", token, expires_at=expiration) 
        supabase_api.add_token(username, token, str(expiration))

    except Exception as e:
        # Display error message outside form context
        st.error(str(e))
        return

    # Display success message outside form context
    st.success("Logged In.", icon="✅")


with form:
    st.text_input("Username", key="username")
    st.text_input("Password", key="password", type="password")
    st.form_submit_button("Log in", on_click=login)

if st.button("Don't have an account? Register one here."):
    st.switch_page("pages/_signup.py")
