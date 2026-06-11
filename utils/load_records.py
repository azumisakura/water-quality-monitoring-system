import pandas as pd
import streamlit as st
from utils.database import supabase

@st.cache_data(show_spinner=False)
def load_records():
    try:
        response = supabase.table("water_quality_records").select("*").execute()

        if getattr(response, "error", None):
            st.error(response.error.message)
            return pd.DataFrame()

        return pd.DataFrame(response.data or [])

    except Exception as exc:
        st.error(f"Unable to load records: {exc}")
        return pd.DataFrame()