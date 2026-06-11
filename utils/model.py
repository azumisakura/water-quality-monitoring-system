import joblib
import streamlit as st

@st.cache_resource
def load_model():
    return joblib.load("water_quality_model (1).pkl")