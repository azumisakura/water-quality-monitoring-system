import streamlit as st
import base64
import os
from components.navbar import show_navbar
show_navbar()

# Background image setup
def get_base64_img(image_path):
    """Safely converts local image to base64 string."""
    # Fallback placeholder if the file is completely missing
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img_base64 = get_base64_img("static/water-bg.jpg")
if img_base64:
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
else:
    st.error(
        "Error: Could not find 'water-bg.jpg'. Place it next to your python script."
    )


st.set_page_config(
    page_title="Water Quality Monitoring System",
    page_icon="💧",
    layout="wide"
)
with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
st.title("Welcome to the Water Quality Monitoring System!")

st.write(
    "Learn more about this web-based application! Kindly explore this website using the navigation bar."
)