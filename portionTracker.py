import streamlit as st
from datetime import date
import pandas as pd

st.title("Portion Tracker")
st.subheader("Upload an image of your meal and EcoNom-y will help you to save money and food!")

tab1,tab2,tab3 = st.tabs(["Before your Meal", "After your Meal","Meal History"])

with tab1:
    uploadCurrent = st.container(border = True)
    with uploadCurrent:
        #Set current date 
        currentDate = date.today().strftime('%B %d, %Y')
        st.subheader(currentDate)
        mealName = st.text_input("What are you having this meal?")
        st.write(mealName)
        st.file_uploader(label="Upload a beautiful picture of your meal!", type = ["png","jpg"])

with tab2:
    mealFeedback = st.container(border = True)
    with mealFeedback:
        st.subheader("Meal Feedback")

        text = "How filling was the meal for your family?"
        # if (numFamilyMembers < 2):
        #     text = "How filling was the meal?"
        # else:
        #     text = "How filling was the meal for your family?"


        feedback = st.selectbox(label=text, options = ["😭 Still very hungry!" , "😔 A little hungry but manageable.", "😁 Perfectly satisfied!", "😒 A little too much.", "🤬 Way too much stuffed!"], index = None)
        feedbackMap = ["😭 Still very hungry!" , "😔 A little hungry but manageable.", "😁 Perfectly satisfied!", "😒 A little too much.", "🤬 Way too much stuffed!"]
        if feedback is not None:
            st.markdown(f"You feel **{feedback}**")

        def hello():
            print("Hello World!")
        
        st.button("Submit", on_click= hello, type="primary")

with tab3:
    # mealPortionHistory = st.container(border=True)
    # with mealPortionHistory:
    #     st.line_chart()
    pass
        
