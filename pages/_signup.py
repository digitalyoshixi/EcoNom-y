import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
from utils.database import get_supabase_api
from utils.auth import require_non_auth

require_non_auth()

supabase_api = get_supabase_api()


st.title("Create a profile")
st.subheader("Make a family profile and start saving your money and the environment")
form = st.form("my_form")


def attempt_sign_up():
    try:
        username = st.session_state.username.strip()
        password = st.session_state.password
        family_size = st.session_state.family_size

        if len(username) == 0 or " " in username or not username.isalnum():
            raise Exception(
                "Enter a valid username. Must be alphanumeric and contain no spaces."
            )
        if len(password) < 8:
            raise Exception("Enter a valid password. 8 characters minimum.")
        if not (0 <= family_size <= 100):
            raise Exception("Enter a valid family size. Minimum 1, maximum 99.")

        supabase_api.create_user(username, password, family_size)

    except Exception as e:
        form.error(e)
        return

    form.success("Account Created. Log In.", icon="✅")


with form:
    st.text_input("Username", key="username")
    st.text_input("Password", key="password", type="password")
    st.number_input(
        "Number of family members",
        key="family_size",
        value=1,
        min_value=1,
        max_value=16,
    )
    st.form_submit_button("Sign Up", on_click=attempt_sign_up)
