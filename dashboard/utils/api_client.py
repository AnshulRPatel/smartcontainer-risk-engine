import requests


API_URL = (
    "https://smartcontainer-risk-engine-api.onrender.com"
)


def predict_shipment(
    payload: dict
):

    response = requests.post(

        f"{API_URL}/predict",

        json=payload,

        timeout=30
    )

    response.raise_for_status()

    return response.json()


def get_health():

    response = requests.get(

        f"{API_URL}/health",

        timeout=10
    )

    response.raise_for_status()

    return response.json()

def explain_shipment(
    payload: dict
):

    response = requests.post(

        f"{API_URL}/explain",

        json=payload,

        timeout=30
    )

    response.raise_for_status()

    return response.json()