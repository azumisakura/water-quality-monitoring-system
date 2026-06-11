import streamlit as st

def show_header():
    st.markdown("""
    <h1 style='text-align:center; color:#1E88E5;'>
    💧 Water Quality Monitoring System
    </h1>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <h4 style='text-align:center; color:gray;'>
    Machine Learning-Based Water Quality Assessment
    </h4>
    """,
    unsafe_allow_html=True
    )

    st.markdown("---")