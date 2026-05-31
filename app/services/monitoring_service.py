from pathlib import Path

from datetime import (
    datetime,
    timezone
)

import pandas as pd


class MonitoringService:

    def __init__(self):

        self.log_path = Path(
            "outputs/monitoring"
        )

        self.log_path.mkdir(

            parents=True,

            exist_ok=True
        )

        self.log_file = (

            self.log_path
            /
            "prediction_logs.csv"
        )

    def log_prediction(

        self,

        container_id,

        prediction
    ):

        log_row = {

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

            "container_id":
            container_id,

            "predicted_risk":
            prediction[
                "predicted_risk"
            ],

            "risk_label":
            prediction[
                "risk_label"
            ],

            "model_confidence":
            prediction[
                "model_confidence"
            ],

            "risk_score":
            prediction[
                "risk_score"
            ],

            "anomaly_score":
            prediction[
                "anomaly_score"
            ]
        }

        df = pd.DataFrame(
            [log_row]
        )

        if self.log_file.exists():

            df.to_csv(

                self.log_file,

                mode="a",

                header=False,

                index=False
            )

        else:

            df.to_csv(

                self.log_file,

                index=False
            )


monitoring_service = (
    MonitoringService()
)