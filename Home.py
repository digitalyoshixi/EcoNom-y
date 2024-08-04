import utils.load_env
from utils.show_sidebar import show_sidebar

show_sidebar()
import streamlit as st

st.markdown("<h1 style='text-align: center;'>EcoNom-y</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center;'>Save Food, Save Money</h3>", unsafe_allow_html=True
)

st.markdown("<h4 style='text-align: left;'>Our Goal:</h4>", unsafe_allow_html=True)
st.markdown(
    "Help consumers reduce their food waste by helping them monitor and reduce overpurchasing of food and ingredients"
)

st.write(
    '_"We often waste good food because we buy too much, don’t plan our meals, or don’t store our food correctly."_'
)
st.write(
    "- City of Toronto, https://www.toronto.ca/services-payments/recycling-organics-garbage/long-term-waste-strategy/waste-reduction/food-waste/"
)

st.markdown(
    "To help consumers reduce food waste, EcoNom-y aims to help with meal planning and ingredient tracking with the use of various emerging technologies"
)
