import joblib

import pandas as pd


class AnomalyService:

    def __init__(self):

        self.model = joblib.load(
            "outputs/models/isolation_forest.pkl"
        )

    def predict_anomaly_score(

        self,

        feature_df
    ):

        score = (

            self.model
            .decision_function(
                feature_df
            )[0]
        )

        return float(score)


anomaly_service = (
    AnomalyService()
)