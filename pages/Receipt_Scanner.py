import streamlit as st
from extra_streamlit_components import CookieManager
from utils.database import get_supabase_api

supabase_api = get_supabase_api()
cookies = CookieManager()


def redirect_to_login():
    st.write("You are not logged in. Redirecting to login page...")
    st.rerun()  # Redirect to login page


def render_file_picker():
    st.title("Upload your file")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("File uploaded successfully")
        # Further file processing logic here


def main():
    token = cookies.get("token")
    if token:
        user_id = supabase_api.verify_token(token)
        if user_id:
            render_file_picker()
        else:
            # redirect_to_login()
            print("Switching page")
            st.switch_page("login.py")

    else:
        redirect_to_login()


main()
