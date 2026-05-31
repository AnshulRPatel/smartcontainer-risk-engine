class ExplainabilityAPIService:

    def extract_risk_factors(

        self,

        prediction,

        processed_df
    ):

        factors = []

        explanation = prediction[
            "explanation"
        ]

        if (
            "high anomaly score"
            in explanation
        ):

            factors.append({

                "factor":
                "high anomaly score",

                "value":
                round(
                    prediction[
                        "anomaly_score"
                    ],
                    4
                )
            })

        if (
            "abnormal weight discrepancy"
            in explanation
            or
            "severe weight discrepancy"
            in explanation
        ):

            factors.append({

                "factor":
                "weight discrepancy (%)",

                "value":
                round(
                    processed_df[
                        "Weight_Difference_Percent"
                    ].iloc[0],
                    2
                )
            })

        if (
            "excessive dwell time"
            in explanation
            or
            "extreme port dwell duration"
            in explanation
        ):

            factors.append({

                "factor":
                "dwell time (hours)",

                "value":
                round(
                    processed_df[
                        "Dwell_Time_Hours"
                    ].iloc[0],
                    2
                )
            })

        if (
            "high cargo value"
            in explanation
            or
            "extremely high cargo value"
            in explanation
        ):

            factors.append({

                "factor":
                "declared value",

                "value":
                round(
                    processed_df[
                        "Declared_Value"
                    ].iloc[0],
                    2
                )
            })

        if (
            "limited importer shipment history"
            in explanation
        ):

            factors.append({

                "factor":
                "importer shipment history",

                "value":
                "low"
            })

        return factors


explainability_api_service = (
    ExplainabilityAPIService()
)