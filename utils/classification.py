import pandas as pd
from utils.model import load_model

rf_model = load_model()

DEFAULT_NO3_N = 7.0       # NO3-N (mg/L)
DEFAULT_PO4_P = 0.5       # PO4-P (mg/L)
DEFAULT_CHLORIDE = 250.0  # Chloride (mg/L)
DEFAULT_COLOR = 75.0      # Color (TCU)


def classify_records(df: pd.DataFrame) -> pd.Series:
    required_db_cols = ["ph", "dissolved_oxygen", "bod", "tss", "temperature"]

    def normalize_classification(series: pd.Series) -> pd.Series:
        mapping = {
            1: "Compliant",
            0: "Non-Compliant",
            "1": "Compliant",
            "0": "Non-Compliant",
            "Compliant": "Compliant",
            "Non-Compliant": "Non-Compliant"
        }
        return series.map(mapping).fillna("Unknown")

    classification_series = pd.Series("Unknown", index=df.index, dtype="string")

    if "classification" in df.columns:
        classification_series = normalize_classification(df["classification"].astype(str))

    if all(col in df.columns for col in required_db_cols):
        compute_mask = df[required_db_cols].notna().all(axis=1)

        if compute_mask.any():
            feature_df = df.loc[compute_mask, required_db_cols].copy()

            feature_df["no3_n"] = DEFAULT_NO3_N
            feature_df["po4_p"] = DEFAULT_PO4_P
            feature_df["chloride"] = DEFAULT_CHLORIDE
            feature_df["color"] = DEFAULT_COLOR

            ordered = [
                "ph",
                "dissolved_oxygen",
                "bod",
                "tss",
                "no3_n",
                "po4_p",
                "temperature",
                "chloride",
                "color"
            ]

            predictions = rf_model.predict(feature_df[ordered].values)

            computed = pd.Series(
                predictions,
                index=feature_df.index
            ).map({
                1: "Compliant",
                0: "Non-Compliant"
            })

            classification_series.loc[compute_mask] = computed

    return classification_series