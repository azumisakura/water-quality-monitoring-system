import streamlit as st
import pandas as pd
import base64
import os

from components.upload_form import show_upload_form
from utils.load_records import load_records
from utils.quality_score import compute_quality_score
from components.navbar import show_navbar

show_navbar()
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
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)
st.html(
    """
    <div style="
        background-color: #2563eb; 
        color: white !important; 
        width: 100%; 
        border-radius: 8px; 
        padding: 12px 20px; 
        font-size: 26px; 
        font-weight: 600; 
        display: flex; 
        align-items: center; 
        gap: 8px;
        box-sizing: border-box;
        margin-bottom: 1rem;
    ">
        Check your water quality status! 📤
    </div>
    """
)

# UPLOAD FORM
show_upload_form()

st.markdown("---")

records_df = load_records()

if not records_df.empty:

    # SUMMARY CARDS
    total_samples = len(records_df)

    compliant_count = (
        records_df["classification"].astype(str).eq("Compliant").sum()
        if "classification" in records_df.columns else 0
    )

    non_compliant_count = (
        records_df["classification"].astype(str).eq("Non-Compliant").sum()
        if "classification" in records_df.columns else 0
    )

    station_count = (
        records_df["location"].nunique()
        if "location" in records_df.columns else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💧 Total Samples", total_samples)
    with col2: st.metric("✅ Compliant", compliant_count)
    with col3: st.metric("❌ Non-Compliant", non_compliant_count)
    with col4: st.metric("📍 Monitoring Stations", station_count)

    # LATEST RECORDS
    st.markdown("---")
    st.html(
        """
        <div style="
            background-color: #2563eb; 
            color: white !important; 
            width: 100%; 
            border-radius: 8px; 
            padding: 12px 20px; 
            font-size: 26px; 
            font-weight: 600; 
            display: flex; 
            align-items: center; 
            gap: 8px;
            box-sizing: border-box;
            margin-bottom: 1rem;
        ">
            📋 Latest Records
        </div>
        """
    )
    latest_df = records_df.tail(5)
    st.dataframe(latest_df, use_container_width=True)

    # OVERALL WATER QUALITY STATUS
    st.markdown("---")
    st.html(
        """
        <div style="
            background-color: #2563eb; 
            color: white !important; 
            width: 100%; 
            border-radius: 8px; 
            padding: 12px 20px; 
            font-size: 26px; 
            font-weight: 600; 
            display: flex; 
            align-items: center; 
            gap: 8px;
            box-sizing: border-box;
            margin-bottom: 1rem;
        ">
            🌊 Overall Water Quality Status
        </div>
        """
    )

    score_df = records_df.copy()
    score_df["quality_score"] = compute_quality_score(score_df)
    overall_score = round(score_df["quality_score"].mean(), 2)

    if overall_score >= 90: status = "🟢 Excellent"
    elif overall_score >= 80: status = "🟢 Good"
    elif overall_score >= 70: status = "🟡 Fair"
    elif overall_score >= 60: status = "🟠 Poor"
    else: status = "🔴 Critical"

    col1, col2 = st.columns(2)
    with col1: st.metric("Average Quality Score", overall_score)
    with col2: st.metric("Overall Status", status)

else:
    st.info("No records available.")
