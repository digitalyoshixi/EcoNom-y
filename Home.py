import utils.load_env
from utils.sidebar import show_sidebar
from utils.auth import is_logged_in

import streamlit as st

#Title and "slogan"
st.markdown("<h1 style='text-align: center;'>EcoNom-y</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center;'>Save Food, Save Money, Save Earth</h3>", unsafe_allow_html=True
)

#Goal and how it could be reached
st.markdown("<h4 style='text-align: left;'>Our Goal:</h4>", unsafe_allow_html=True)
st.markdown(
    "Help consumers reduce their food waste by helping them monitor and reduce overpurchasing of food and ingredients."
)

#Food waste image and statement
st.image("https://d1wawsg0a7g34j.cloudfront.net/d56d8a681b03deafe36b22df7d22ab73.jpg")
st.write(
    '_"We often waste good food because we buy too much, don’t plan our meals, or don’t store our food correctly."_'
)
st.write(
    "- City of Toronto, https://www.toronto.ca/services-payments/recycling-organics-garbage/long-term-waste-strategy/waste-reduction/food-waste/"
)

#Brief rundown of the application
st.markdown(
    "<h5 style='text-align: center;'>To help consumers reduce food waste, EcoNom-y aims to provide various features such as meal planning and portion tracking with the use of various emerging technologies</h5>",  unsafe_allow_html=True
)

#Making columns and their containers
col1, col2, col3 = st.columns(3, gap = "medium")
tile1 = col1.container(height=300)
tile2 = col2.container(height=300)
tile3 = col3.container(height=300)

#Listing features
with tile1:
    st.subheader("Look for recipes")
    st.write("With the help of Artificial Intelligence, get a recipe suggestion based off keyword(s), or generate something commpletely new to try")

with tile2:
    st.subheader("Scan your receipts")
    st.write("Once you are done shopping for ingredients, scan your receipt to keep track of your ingredients and be reminded before their expiry date")

with tile3:
    st.subheader("Track portion sizes")
    st.write("After trying your new recipe, provide feedback on whether or not the portion sizes for that dish were too much or too little, and adjust thme down the line")

#Only give this if its someone who isnt signed in

if is_logged_in() == False:
    col2.page_link("pages/_signup.py", label="Create an account today")
    col2.text("")
    col2.page_link("pages/_login.py", label="Log in with an account")
else:
    show_sidebar()