import streamlit as st
from extra_streamlit_components import CookieManager
#from pages import Portion_Tracker, login, Recipe_Bank, signup

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# @st.cache_resource
# def get_manager():
#     return stx.CookieManager()

cookie_manager = CookieManager()
cookies = cookie_manager.get_all()
cookie_manager.set("token", 19191)


# if 'token' not in st.session_state:
#     st.session_state.token = 0 # nothing. will not validate anything at all

st.write("Welcome to my app")