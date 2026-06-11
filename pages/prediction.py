import streamlit as st
import numpy as np
import pandas as pd
from utils.model import load_model
from utils.database import supabase
import base64
import os

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

# Load Random Forest model
rf_model = load_model()

# Default values (same as Dashboard)
DEFAULT_NO3_N = 7.0
DEFAULT_PO4_P = 0.5
DEFAULT_CHLORIDE = 250.0
DEFAULT_COLOR = 75.0

st.markdown("<h1 style='text-align: center;'>💧 Water Quality Prediction</h1>", unsafe_allow_html=True)
st.html(
            """
            <div style="
                background-color: #2563eb; 
                color: white !important; 
                width: 100%; 
                border-radius: 8px; 
                padding: 12px 20px; 
                font-size: 24px; 
                font-weight: 600; 
                display: flex; 
                align-items: center; 
                gap: 8px;
                box-sizing: border-box;
                margin-bottom: 1rem;
            ">
                Machine Learning-Based Water Classification
            </div>
            """
        )

# Custom CSS for wider container and smaller summary
st.markdown(
    """
    <style>
    /* Palakihin ang main container */
    div[data-testid="stContainer"] {
        background-color: white;
        padding: 50px;
        border-radius: 25px;
        box-shadow:
            0 12px 30px rgba(0,0,0,0.12),
            inset 0 2px 0 rgba(255,255,255,0.9);
        margin-top: 30px;
        margin-bottom: 30px;
        max-width: 98%;        /* mas malapad ang container */
        margin-left: auto;
        margin-right: auto;
    }

    /* Mas maliit na font para sa Input Summary at Interpretation */
    .small-text {
        font-size: 13px;
        color: #444444;
    }

    .small-table td, .small-table th {
        font-size: 13px !important;
        padding: 4px 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Isang malaking embossed container
with st.container(border=True):
    left_col, right_col = st.columns([2,1])

    with left_col:
        st.subheader("Input Water Parameters")

        ph = st.number_input("pH Level", min_value=0.0, step=0.1)
        bod = st.number_input("Biochemical Oxygen Demand (BOD, mg/L)", min_value=0.0, step=0.1)
        dissolved_oxygen = st.number_input("Dissolved Oxygen (mg/L)", min_value=0.0, step=0.1)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, step=0.1)
        tss = st.number_input("Total Suspended Solids (TSS, mg/L)", min_value=0.0, step=0.1)
        fecal_coliform = st.number_input("Fecal Coliform (CFU/100mL)", min_value=0.0, step=1.0)

        if st.button("Predict Classification"):
            if ph == 0:
                st.error("pH cannot be 0")
            elif dissolved_oxygen == 0:
                st.error("Dissolved Oxygen cannot be 0")
            elif bod == 0:
                st.error("BOD cannot be 0")
            elif tss == 0:
                st.error("TSS cannot be 0")
            elif fecal_coliform == 0:
                st.error("Fecal Coliform cannot be 0")
            else:
                features = np.array([[
                    ph,
                    dissolved_oxygen,
                    bod,
                    tss,
                    DEFAULT_NO3_N,
                    DEFAULT_PO4_P,
                    temperature,
                    DEFAULT_CHLORIDE,
                    DEFAULT_COLOR
                ]])

                prediction = rf_model.predict(features)[0]
                classification = "Compliant" if prediction == 1 else "Non-Compliant"

                probabilities = rf_model.predict_proba(features)[0]
                confidence = round(max(probabilities) * 100, 2)

                st.session_state["classification"] = classification
                st.session_state["confidence"] = confidence
                st.session_state["data"] = {
                    "ph": ph,
                    "bod": bod,
                    "dissolved_oxygen": dissolved_oxygen,
                    "temperature": temperature,
                    "tss": tss,
                    "fecal_coliform": int(fecal_coliform),
                    "classification": classification
                }

    with right_col:
        st.subheader("Prediction Result")

        if "classification" in st.session_state:
            classification = st.session_state["classification"]
            confidence = st.session_state["confidence"]

            if classification == "Compliant":
                st.success("✅ COMPLIANT")
            else:
                st.error("❌ NON-COMPLIANT")

            st.metric("🎯 Prediction Confidence", f"{confidence}%")
            st.progress(confidence / 100)

            st.info("🤖 Algorithm Used: Random Forest Classifier")

            # Input Summary (smaller)
            st.markdown('<p class="small-text">Input Summary</p>', unsafe_allow_html=True)
            summary_df = pd.DataFrame({
                "Parameter": [
                    "pH",
                    "DO (mg/L)",
                    "BOD (mg/L)",
                    "TSS (mg/L)",
                    "Temperature (°C)",
                    "Fecal Coliform (CFU/100mL)"
                ],
                "Value": [
                    st.session_state["data"]["ph"],
                    st.session_state["data"]["dissolved_oxygen"],
                    st.session_state["data"]["bod"],
                    st.session_state["data"]["tss"],
                    st.session_state["data"]["temperature"],
                    st.session_state["data"]["fecal_coliform"]
                ]
            })
            st.dataframe(summary_df, use_container_width=True, height=120)

            # Interpretation (smaller)
            st.markdown('<p class="small-text">💡 Interpretation</p>', unsafe_allow_html=True)
            if classification == "Compliant":
                st.markdown(
                    '<p class="small-text">The water sample satisfies the acceptable standards and is classified as compliant.</p>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<p class="small-text">The water sample does not satisfy the acceptable standards and is classified as non-compliant.</p>',
                    unsafe_allow_html=True
                )

# Save Sample button
if "data" in st.session_state:
    if st.button("Save Sample"):
        try:
            response = (
                supabase
                .table("water_quality_records")
                .insert(st.session_state["data"])
                .execute()
            )
            if response.data:
                st.success("Sample saved successfully! 🎉")
                del st.session_state["data"]
            else:
                st.error("Failed to save sample.")
        except Exception as e:
            st.error(f"Error: {e}")
