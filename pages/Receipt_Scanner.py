import streamlit as st
from PIL import Image
from utils.auth import require_auth

require_auth()
from utils.sidebar import show_sidebar

show_sidebar()
from utils.receipt import ReceiptParser

# Initialize the receipt parser
receipt_parser = ReceiptParser()


# Initialize session state variables
if "image_uploaded" not in st.session_state:
    st.session_state.image_uploaded = False

# Display the title above the form
if not st.session_state.image_uploaded:
    st.title("Upload your file")
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:
        st.session_state.image_uploaded = True
        st.session_state.uploaded_file = uploaded_file
else:
    uploaded_file = st.session_state.uploaded_file

if uploaded_file is not None:
    st.title("Your Receipt")
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    # Parse the receipt and display the ingredients
    ingredients = receipt_parser.parse_receipt(image)
    for ingredient in ingredients:
        st.write(ingredient)
