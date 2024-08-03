import streamlit as st
from datetime import date


st.title("Portion Tracker")
st.subheader(
    "Upload an image of your meal and EcoNom-y will help you to save money and food!")


uploadCurrent = st.container(border=True)
with uploadCurrent:
    currentDate = date.today().strftime('%B %d, %Y')
    st.subheader(currentDate)
    mealName = st.text_input("What are you having this meal?")
    st.write(mealName)
    st.file_uploader(
        label="Upload a beautiful picture of your meal!",
        type=[
            "png",
            "jpg"])

mealFeedback = st.container(border=True)
with mealFeedback:
    st.subheader("Meal Feedback")

    text = "How filling was the meal for your family?"
    # if (numFamilyMembers < 2):
    #     text = "How filling was the meal?"
    # else:
    #     text = "How filling was the meal for your family?"

    st.write(text)
    feedback = st.feedback(options="faces")
    feedbackMapping = [
        "still pretty hungry 😤",
        "a little bit hungry but manageable",
        "perfectly satisfied",
        "a little too much",
        "way too much food 😡"]
    if feedback is not None:
        st.markdown(f"You feel *{feedbackMapping[feedback]}*")


# image upload (picture of your meal)
