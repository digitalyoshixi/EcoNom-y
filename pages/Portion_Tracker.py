from utils.auth import require_auth

require_auth()
from utils.sidebar import show_sidebar

show_sidebar()
import streamlit as st
from datetime import date
from utils.database import get_supabase_api

supabaseAPI = get_supabase_api()

st.title("Portion Tracker")
st.subheader(
    "Upload an image of your meal and EcoNom-y will help you to save money and food!"
)

uploadCurrent = st.container(border=True)
with uploadCurrent:
    currentDate = date.today().strftime("%B %d, %Y")
    st.subheader(currentDate)
    mealName = st.text_input("What are you having this meal?")
    st.write(mealName)
    st.file_uploader(
        label="Upload a beautiful picture of your meal!", type=["png", "jpg"]
    )

mealFeedback = st.container(border=True)
with mealFeedback:
    st.subheader("Meal Feedback")

    text = "How filling was the meal for your family?"
    # numFamilyMembers = supabaseAPI.selectspecific()
    # if (numFamilyMembers < 2):
    #     text = "How filling was the meal?"
    # else:
    #     text = "How filling was the meal for your family?"

    st.write(text)
    feedback = st.selectbox(
        text,
        [
            "way too little food!" + "😔",
            "not enough food but it's manageable.",
            "the perfect amount of food!" + "😁",
            "a little too much food.",
            "way too much food" + "😡",
        ],
        index=None,
    )

    if feedback is not None:
        st.markdown(f"This time there was *{feedback}*")
