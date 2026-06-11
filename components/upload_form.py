import streamlit as st
import numpy as np

from utils.model import load_model
from utils.database import supabase

# Load Random Forest model once
rf_model = load_model()

DEFAULT_NO3_N = 7.0
DEFAULT_PO4_P = 0.5
DEFAULT_CHLORIDE = 250.0
DEFAULT_COLOR = 75.0

def show_upload_form():
    with st.form("upload_form"):
        month = st.text_input("Month (January, February, etc.)")
        location = st.text_input("Location")
        st.markdown("### Water Parameters")
        ph = st.number_input("pH (0–14)", min_value=0.0, max_value=14.0, step=0.01)
        bod = st.number_input("BOD (must not be 0)", min_value=0.0, step=0.01)
        dissolved_oxygen = st.number_input("Dissolved Oxygen (must not be 0)", min_value=0.0, step=0.01)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=45.0, value=0.0, step=0.1)
        tss = st.number_input("TSS (must not be 0)", min_value=0.0, step=0.01)
        fecal_coliform = st.number_input("Fecal Coliform (must not be 0)", min_value=0, step=1)
        submit = st.form_submit_button("Save Sample")

    if submit:
        try:
            if not month or not location:
                st.error("Please fill in Month and Location")
            elif ph == 0:
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
                # Correct feature order
                features = np.array([[ph, dissolved_oxygen, bod, tss,
                                      DEFAULT_NO3_N, DEFAULT_PO4_P,
                                      temperature, DEFAULT_CHLORIDE, DEFAULT_COLOR]])
                prediction = rf_model.predict(features)[0]
                classification = "Compliant" if prediction == 1 else "Non-Compliant"
                st.write("Probabilities:", rf_model.predict_proba(features))

                data = {
                    "month": month,
                    "location": location,
                    "ph": ph,
                    "bod": bod,
                    "dissolved_oxygen": dissolved_oxygen,
                    "temperature": temperature,
                    "tss": tss,
                    "fecal_coliform": int(fecal_coliform),
                    "classification": classification
                }

                response = supabase.table("water_quality_records").insert(data).execute()
                if response.data:
                    st.success("Sample saved successfully! 🎉")
                    st.info(f"Classification: {classification}")
                else:
                    st.error("Failed to save data")
        except Exception as e:
            st.exception(e)