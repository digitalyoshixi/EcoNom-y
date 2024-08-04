import utils.load_env
import streamlit as st
from extra_streamlit_components import CookieManager

# from pages import Portion_Tracker, login, Recipe_Bank, signup

st.markdown("<h1 style='text-align: center;'>EcoNom-y</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center;'>Save Food, Save Money</h3>", unsafe_allow_html=True
)

st.markdown("<h4 style='text-align: left;'>Our Goal:</h4>",
            unsafe_allow_html=True)
st.markdown("Help consumers reduce their food waste")

# @st.cache_resource
# def get_manager():
#     return stx.CookieManager()

cookie_manager = CookieManager()
cookies = cookie_manager.get_all()
print(cookies)
# cookie_manager.set("token", 19191)
# cookies = CookieManager
cookies.delete("key")
cookies = cookie_manager.get_all()
print(cookies)

# if 'token' not in st.session_state:
#     st.session_state.token = 0 # nothing. will not validate anything at all
