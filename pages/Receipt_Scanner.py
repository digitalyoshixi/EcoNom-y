import utils.require_auth
from utils.show_sidebar import show_sidebar

show_sidebar()
show_sidebar()
import streamlit as st

st.title("Upload your file")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully")
