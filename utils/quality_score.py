import pandas as pd

# Compute a quality score based on available parameters
def compute_quality_score(df: pd.DataFrame) -> pd.Series:
    score = pd.Series(0.0, index=df.index)
    count = 0

    if "ph" in df:
        score += 1 - (df["ph"].sub(7.5).abs().clip(upper=6.5) / 6.5)
        count += 1

    if "dissolved_oxygen" in df:
        score += (df["dissolved_oxygen"] / 15).clip(0, 1)
        count += 1

    if "bod" in df:
        score += (1 - (df["bod"] / 20).clip(0, 1))
        count += 1

    if "tss" in df:
        score += (1 - (df["tss"] / 100).clip(0, 1))
        count += 1

    if "temperature" in df:
        score += (1 - (df["temperature"].sub(25).abs() / 20).clip(0, 1))
        count += 1

    if "fecal_coliform" in df:
        score += (1 - (df["fecal_coliform"] / 1000).clip(0, 1))
        count += 1

    if count == 0:
        return score

    return (score / count * 100).clip(0, 100)