import streamlit as st
from utils.database import get_supabase_api

supabase_api = get_supabase_api()


def showpage():
    st.title("Create a profile")
    st.subheader(
        "Make a family profile and start saving your money and the environment"
    )
    form = st.form("my_form")

    def createProfile():
        username = st.session_state.un
        password = st.session_state.pw
        size = st.session_state.family
        validity = True
        if len(username) == 0:
            form.error("Enter a valid username")
            validity = False
        if len(password) == 0:
            form.error("Enter a valid password")
            validity = False
        if len(size) == 0:
            form.error("Enter a valid family size")
            validity = False

        if validity:
            supabase_api.add_user(username, password, size)
            form.success("Account Created")

    with form:
        st.text_input("Username", key="un")
        st.text_input("Password", key="pw", type="password")
        st.number_input(
            "Number of family members", key="family", value=1, min_value=1, max_value=16
        )
        st.form_submit_button("Create Account", on_click=createProfile)
