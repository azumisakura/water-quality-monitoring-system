import streamlit as st


def show_table(display_df):
    st.dataframe(
        display_df,
        use_container_width=True
    )