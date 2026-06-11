import streamlit as st

def show_filters(records_df):
    parameter_labels = {
        "ph": "pH",
        "bod": "Biochemical Oxygen Demand (BOD)",
        "dissolved_oxygen": "Dissolved Oxygen",
        "temperature": "Temperature (°C)",
        "tss": "Total Suspended Solids (TSS)",
        "fecal_coliform": "Fecal Coliform"
    }

    numeric_parameters = [
        "ph",
        "bod",
        "dissolved_oxygen",
        "temperature",
        "tss",
        "fecal_coliform"
    ]

    available_fields = [
        p for p in numeric_parameters
        if p in records_df.columns
    ]

    available_labels = [
        parameter_labels[p]
        for p in available_fields
    ]

    selected_label = st.selectbox(
        "Select a water quality parameter",
        available_labels
    )

    selected_parameter = available_fields[
        available_labels.index(selected_label)
    ]

    station_options = []

    if "location" in records_df.columns:
        station_options = sorted(
            records_df["location"]
            .dropna()
            .astype(str)
            .unique()
        )

    station_selection = st.multiselect(
        "Select monitoring stations",
        station_options,
        default=[]
    )

    month_options = []

    if "month" in records_df.columns:
        all_months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        normalized_months = {
            str(m).strip().capitalize()
            for m in records_df["month"].dropna().astype(str)
        }

        month_options = sorted(
            normalized_months,
            key=lambda m: all_months.index(m)
            if m in all_months else 12
        )

    month_selection = st.multiselect(
        "Select months",
        month_options,
        default=[]
    )

    return (
        selected_parameter,
        station_selection,
        month_selection,
        parameter_labels
    )