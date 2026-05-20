import numpy as np


def generate_pseudo_labels(df):

    critical_threshold = (
        df["Total_Risk_Score"]
        .quantile(0.98)
    )

    medium_threshold = (
        df["Total_Risk_Score"]
        .quantile(0.85)
    )

    df["Risk_Label"] = np.select(
        [
            df["Total_Risk_Score"] >= critical_threshold,
            df["Total_Risk_Score"] >= medium_threshold
        ],
        [
            "Critical",
            "Medium"
        ],
        default="Low"
    )

    return df