import streamlit as st

def show_navbar():

    st.markdown("""
    <style>

    .navbar{
        background: linear-gradient(90deg,#1877f2,#0ea5a8);
        padding:15px 25px;
        border-radius:0px;
        margin-bottom:20px;
    }

    .title{
        color:white !important;
        font-size:32px;
        font-weight:bold;
        margin-bottom:5px;
    }

    .subtitle{
        color:white !important;
        font-size:15px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="navbar" style="text-align: center; width: 100%;">
        <div class="title">💧 Water Quality Monitor</div>
        <div class="subtitle">Imus Environmental Data</div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.page_link(
            "app.py",
            label="Home"
        )

    with col2:
        st.page_link(
            "pages/dashboard.py",
            label="Dashboard"
        )

    with col3:
        st.page_link(
            "pages/visualization.py",
            label="Data Visualization"
        )

    with col4:
        st.page_link(
            "pages/prediction.py",
            label="Prediction"
        )

    with col5:
        st.page_link(
            "pages/about.py",
            label="About"
        )

    st.markdown("---")