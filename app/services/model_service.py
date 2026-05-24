import pandas as pd

from ml.modeling.inference import (
    load_model
)

from ml.modeling.preprocess import (
    prepare_inference_data
)

from app.utils.inference_utils import (
    decode_prediction
)


class ModelService:

    def __init__(self):

        self.model = load_model()

    def predict(self, shipment):

        # =========================
        # RAW INPUT
        # =========================

        raw_df = pd.DataFrame(
            [shipment]
        )

        # =========================
        # PREPROCESS
        # =========================

        processed_df = (
            prepare_inference_data(
                raw_df
            )
        )

        # =========================
        # PREDICT
        # =========================

        prediction = (

            self.model.predict(
                processed_df
            )[0]
        )

        probabilities = (

            self.model.predict_proba(
                processed_df
            )[0]
        )

        risk_score = float(
            max(probabilities)
        )

        decoded_risk = (
            decode_prediction(
                prediction
            )
        )

        # =========================
        # PLACEHOLDER EXPLANATION
        # =========================

        explanation = (

            f"Shipment classified as "
            f"{decoded_risk} risk "
            f"based on operational "
            f"and anomaly indicators."
        )

        return {

            "predicted_risk": (
                decoded_risk
            ),

            "risk_score": (
                risk_score
            ),

            "anomaly_score": 0.0,

            "explanation": (
                explanation
            )
        }


model_service = ModelService()