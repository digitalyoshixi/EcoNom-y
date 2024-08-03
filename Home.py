import streamlit as st
#from pages import Portion_Tracker, login, Recipe_Bank, signup

<<<<<<< HEAD
st.markdown("<h1 style='text-align: center;'>EcoNom-y</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Save Food, Save Money</h3>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: left;'>Our Goal:</h4>", unsafe_allow_html=True)
st.markdown("Help consumers reduce their food waste")
#if st.session_state.token == None:
    #st.session_state.token = 0 # nothing. will not validate anything at all

=======
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
if 'token' not in st.session_state:
    st.session_state.token = 0 # nothing. will not validate anything at all
>>>>>>> 8ec32b1bb0bb9dc617a49a4c66c7efd98a27e269

