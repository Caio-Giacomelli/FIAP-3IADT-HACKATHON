import streamlit as st
from PIL import Image

# Generic title and subtitle
st.title("Architecture Diagram Analyzer")
st.subheader("Upload your system architecture diagram for analysis")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Submit button
if st.button("Submit"):
    if uploaded_file is not None:
        # Display image preview
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.success("Image submitted successfully!")
    else:
        st.warning("Please upload an image before submitting.")
