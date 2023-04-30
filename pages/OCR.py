import streamlit as st



my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])