import numpy as np

import json

from pathlib import Path

def generate_pseudo_labels(df):

    critical_threshold = (
        df["Total_Risk_Score"]
        .quantile(0.98)
    )

    medium_threshold = (
        df["Total_Risk_Score"]
        .quantile(0.85)
    )

    # ==========================================
    # SAVE THRESHOLDS FOR INFERENCE
    # ==========================================

    artifact_dir = Path(
        "outputs/artifacts"
    )

    artifact_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    thresholds = {

        "critical_threshold":
        float(
            critical_threshold
        ),

        "medium_threshold":
        float(
            medium_threshold
        )
    }

    with open(

        artifact_dir /
        "risk_label_thresholds.json",

        "w"
    ) as f:

        json.dump(

            thresholds,

            f,

            indent=4
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