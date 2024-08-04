import streamlit as st
import pandas as pd
from utils.food_banks import FoodBanks

#flat, flng
food_banks = FoodBanks()
query = food_banks.locate_food_banks("Toronto Metropolitian University")


df = pd.DataFrame({
    "col1": [query['closest_food_banks'][0]['flat'], query['closest_food_banks'][1]['flat']],
    "col2": [query['closest_food_banks'][0]['flng'], query['closest_food_banks'][1]['flng']]})

st.title("Food Banks Nearby")
st.subheader("Donate unwanted ingredients")

st.map(df,
    latitude='col1',
    longitude='col2')