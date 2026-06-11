from utils.classification import classify_records

def prepare_display_data(filtered_df):

    filtered_df = filtered_df.reset_index(drop=True)

    filtered_df["classification"] = classify_records(
        filtered_df
    )

    column_renames = {
        "month": "Month",
        "location": "Monitoring Station",
        "ph": "pH",
        "bod": "BOD (mg/L)",
        "dissolved_oxygen": "Dissolved Oxygen (mg/L)",
        "temperature": "Temperature (°C)",
        "tss": "TSS (mg/L)",
        "fecal_coliform": "Fecal Coliform (CFU/100mL)",
        "classification": "Classification"
    }

    selected_columns = [
        col
        for col in column_renames.keys()
        if col in filtered_df.columns
    ]

    display_df = filtered_df[selected_columns].rename(
        columns={
            k: v
            for k, v in column_renames.items()
            if k in selected_columns
        }
    )

    return filtered_df, display_df

