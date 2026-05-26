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

from app.services.context_service import (
    context_service
)

from app.services.risk_calibration_service import (
    risk_calibration_service
)

from app.services.explanation_service import (
    explanation_service
)

from app.services.risk_label_service import (
    risk_label_service
)

class ModelService:

    def __init__(self):

        # =================================================
        # LOAD TRAINED MODEL ONCE
        # =================================================

        self.model = load_model()

    # =====================================================
    # SINGLE PREDICTION
    # =====================================================

    def predict(

        self,

        shipment
    ):

        # ================================================
        # RAW INPUT
        # ================================================

        raw_df = pd.DataFrame(
            [shipment]
        )

        # ================================================
        # CONTEXTUAL FEATURE ENGINEERING
        # ================================================

        processed_df = (
            prepare_inference_data(

                raw_df,

                context_service=
                context_service
            )
        )
        print("\n========== API FEATURE MATRIX ==========\n")

        print(processed_df.T)
        # ================================================
        # MODEL PREDICTION
        # ================================================

        prediction = (

            self.model.predict(
                processed_df
            )[0]
        )

        print("\n========== MODEL DEBUG ==========\n")

        print("Raw Prediction:")
        print(prediction)

        

        probabilities = (

            self.model.predict_proba(
                processed_df
            )[0]
        )

        print("\nPrediction Probabilities:")
        print(probabilities)

        model_confidence = float(
        max(probabilities)
        )

        # ================================================
        # DECODE LABEL
        # ================================================

        decoded_risk = (
            decode_prediction(
                prediction
            )
        )

        print("\nDecoded Risk:")
        print(decoded_risk)

        # ================================================
        # ANOMALY SCORE
        # ================================================

        anomaly_score = float(

            processed_df[
                "Anomaly_Score"
            ].iloc[0]
        )

        # ================================================
        # FEATURE EXTRACTION
        # ================================================

        weight_diff_percent = abs(

            processed_df[
                "Weight_Difference_Percent"
            ].iloc[0]
        )

        dwell_time = (

            processed_df[
                "Dwell_Time_Hours"
            ].iloc[0]
        )

        exporter_count = (

            processed_df[
                "Exporter_Shipment_Count"
            ].iloc[0]
        )

        shipping_frequency = (

            processed_df[
                "Shipping_Line_Frequency"
            ].iloc[0]
        )

        route_risk = (

            context_service
            .estimate_route_risk(

                shipment[
                    "Origin_Country"
                ],

                shipment[
                    "Destination_Country"
                ]
            )
        )

        # ================================================
        # CALIBRATED OPERATIONAL RISK SCORE
        # ================================================

        risk_score = (

            risk_calibration_service
            .calculate_operational_risk(

                declared_value=
                shipment["Declared_Value"],

                weight_diff_percent=
                weight_diff_percent,

                dwell_time=
                dwell_time,

                importer_count=
                context_service
                .get_importer_shipment_count(

                    shipment[
                        "Importer_ID"
                    ]
                ),

                is_night_declaration=
                processed_df[
                    "Is_Night_Declaration"
                ].iloc[0],

                was_zero_declared_weight=
                processed_df[
                    "was_zero_declared_weight"
                ].iloc[0],

                was_zero_declared_value=
                0,

                route_risk_score=
                route_risk
            )
        )
        # ==========================================
        # RULE-BASED RISK LABEL
        # ==========================================

        risk_label = (
            risk_label_service
            .get_risk_label(
                risk_score
            )
        )

        # ================================================
        # DYNAMIC EXPLANATION ENGINE
        # ================================================

        explanation_row = {

            "Risk_Label":
            decoded_risk,

            "Anomaly_Score":
            anomaly_score,

            "Declared_Value":
            shipment["Declared_Value"],

            "Weight_Difference_Percent":
            processed_df[
                "Weight_Difference_Percent"
            ].iloc[0],

            "Dwell_Time_Hours":
            processed_df[
                "Dwell_Time_Hours"
            ].iloc[0],

            "Is_Night_Declaration":
            processed_df[
                "Is_Night_Declaration"
            ].iloc[0],

            "Importer_Shipment_Count":
            context_service
            .get_importer_shipment_count(

                shipment[
                    "Importer_ID"
                ]
            )
        }

        explanation = (
            explanation_service
            .generate_explanation(
                explanation_row
            )
        )

        # ================================================
        # FINAL RESPONSE
        # ================================================

        return {

            "predicted_risk":
            decoded_risk,

            "risk_label":
            risk_label,

            "model_confidence":
            round(
                model_confidence,
                3
            ),

            "risk_score":
            risk_score,

            "anomaly_score":
            anomaly_score,

            "explanation":
            explanation
        }

    # =====================================================
    # BATCH PREDICTION
    # =====================================================

    def batch_predict(

        self,

        shipment_list
    ):

        results = []

        for shipment in shipment_list:

            result = (
                self.predict(
                    shipment
                )
            )

            results.append(result)

        return results


# =========================================================
# SINGLETON INSTANCE
# =========================================================

model_service = ModelService()