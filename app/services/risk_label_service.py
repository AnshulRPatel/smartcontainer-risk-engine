import json

from pathlib import Path


class RiskLabelService:

    def __init__(self):

        threshold_file = Path(
            "outputs/artifacts/risk_label_thresholds.json"
        )

        with open(
            threshold_file,
            "r"
        ) as f:

            thresholds = json.load(f)

        self.critical_threshold = (
            thresholds[
                "critical_threshold"
            ]
        )

        self.medium_threshold = (
            thresholds[
                "medium_threshold"
            ]
        )

    def get_risk_label(
        self,
        risk_score
    ):

        risk_score = round(
            float(risk_score),
            6
        )

        self.critical_threshold = round(
            float(self.critical_threshold),
            6
        )

        self.medium_threshold = round(
            float(self.medium_threshold),
            6
        )

        if risk_score >= self.critical_threshold:

            return "Critical"

        elif risk_score >= self.medium_threshold:

            return "Medium"

        return "Low"


risk_label_service = (
    RiskLabelService()
)