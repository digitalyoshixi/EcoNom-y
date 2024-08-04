import streamlit as st
import pandas as pd
from utils.food_banks import FoodBanks

#flat, flng
food_banks = FoodBanks()
query = food_banks.locate_food_banks("Toronto Metropolitian University")
col1 = []
col2 = []

for food_bank in query['closest_food_banks']:
    col1.append(food_bank['flat'])
    col2.append(food_bank['flng'])

df = pd.DataFrame({
    "col1": col1,
    "col2": col2})

st.title("Food Banks Nearby")
st.subheader("Donate unwanted ingredients")

st.map(df,
    latitude='col1',
    longitude='col2')