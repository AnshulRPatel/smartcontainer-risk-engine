import json


def save_risk_thresholds(

    value_threshold_95,
    value_threshold_99,
    dwell_threshold_95,
    importer_threshold_10
):

    thresholds = {

        "value_threshold_95":
        float(value_threshold_95),

        "value_threshold_99":
        float(value_threshold_99),

        "dwell_threshold_95":
        float(dwell_threshold_95),

        "importer_threshold_10":
        float(importer_threshold_10)
    }

    with open(

        "outputs/artifacts/risk_thresholds.json",

        "w"
    ) as f:

        json.dump(

            thresholds,

            f,

            indent=4
        )

    print(
        "\nRisk thresholds saved."
    )