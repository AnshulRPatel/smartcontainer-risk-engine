RISK_MAPPING = {

    0: "Critical",

    1: "Low",

    2: "Medium"
}


def decode_prediction(prediction):

    return RISK_MAPPING.get(
        int(prediction),
        "Unknown"
    )