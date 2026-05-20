def compute_total_risk_score(df):

    # Normalize all risk components to ~0–1 range

    df["Normalized_Weight_Risk"] = (
        df["Weight_Risk_Score"] / 3
    )

    df["Normalized_Value_Risk"] = (
        df["Value_Risk_Score"] / 3
    )

    df["Normalized_Dwell_Risk"] = (
        df["Dwell_Risk_Score"] / 2
    )

    df["Normalized_Route_Risk"] = (
        df["Route_Risk_Score"] / 2
    )

    df["Normalized_Behavioral_Risk"] = (
        df["Behavioral_Risk_Score"] / 3
    )

    df["Normalized_Temporal_Risk"] = (
        df["Temporal_Risk_Score"] / 2
    )

    df["Normalized_Integrity_Risk"] = (
        df["Integrity_Risk_Score"] / 3
    )

    # Weighted hybrid operational risk score

    df["Total_Risk_Score"] = (
        0.30 * df["Normalized_Weight_Risk"]
        +
        0.25 * df["Normalized_Value_Risk"]
        +
        0.20 * df["Normalized_Dwell_Risk"]
        +
        0.10 * df["Normalized_Route_Risk"]
        +
        0.10 * df["Normalized_Behavioral_Risk"]
        +
        0.03 * df["Normalized_Temporal_Risk"]
        +
        0.02 * df["Normalized_Integrity_Risk"]
    )

    return df