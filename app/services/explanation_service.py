import json

from pathlib import Path

from ml.explainability.generate_explanations import (
    build_explanation
)


class ExplanationService:

    def __init__(self):

        threshold_file = Path(
            "outputs/artifacts/risk_thresholds.json"
        )

        with open(
            threshold_file,
            "r"
        ) as f:

            thresholds = json.load(f)

        self.q95_value = (
            thresholds[
                "value_threshold_95"
            ]
        )

        self.q99_value = (
            thresholds[
                "value_threshold_99"
            ]
        )

        self.dwell_threshold = (
            thresholds[
                "dwell_threshold_95"
            ]
        )

        self.importer_threshold = (
            thresholds[
                "importer_threshold_10"
            ]
        )

    def generate_explanation(

        self,

        row
    ):

        return build_explanation(

            row=row,

            q95_value=
            self.q95_value,

            q99_value=
            self.q99_value,

            dwell_threshold=
            self.dwell_threshold,

            importer_threshold=
            self.importer_threshold
        )


explanation_service = (
    ExplanationService()
)