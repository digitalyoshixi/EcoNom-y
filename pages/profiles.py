import streamlit as st

st.title("Create a profile")
st.subheader("Make a family profile and start saving your money and the environment")

def createProfile():
    username = st.session_state.un
    password = st.session_state.pw
    
    size = st.session_state.family
    print("Username: " + username)


with st.form(key="my_form"):
    st.text_input("Username", key="un")
    st.text_input("Password", key="pw", type = "password")
    st.text_input("Number of family members", key="family")
    st.form_submit_button("Create Account", on_click=createProfile)