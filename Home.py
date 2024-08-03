import streamlit as st
#from pages import Portion_Tracker, login, Recipe_Bank, signup

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
if st.session_state.token == None:
    st.session_state.token = 0 # nothing. will not validate anything at all

st.write("Welcome to my app")