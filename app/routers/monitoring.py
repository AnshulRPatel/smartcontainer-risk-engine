import pandas as pd

from pathlib import Path

from fastapi import APIRouter


router = APIRouter()


@router.get(
    "/monitoring/summary"
)
def monitoring_summary():

    log_file = Path(
        "outputs/monitoring/prediction_logs.csv"
    )

    if not log_file.exists():

        return {

            "total_predictions": 0
        }

    df = pd.read_csv(
        log_file
    )

    return {

        "total_predictions":
        len(df),

        "critical_predictions":
        int(
            (
                df[
                    "predicted_risk"
                ]
                ==
                "Critical"
            ).sum()
        ),

        "medium_predictions":
        int(
            (
                df[
                    "predicted_risk"
                ]
                ==
                "Medium"
            ).sum()
        ),

        "low_predictions":
        int(
            (
                df[
                    "predicted_risk"
                ]
                ==
                "Low"
            ).sum()
        ),

        "average_confidence":
        round(

            df[
                "model_confidence"
            ].mean(),

            3
        ),

        "average_risk_score":
        round(

            df[
                "risk_score"
            ].mean(),

            3
        )
    }