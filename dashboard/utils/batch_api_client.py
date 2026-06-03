import requests


API_URL = (
    "http://localhost:8000"
)


def batch_predict_csv(
    uploaded_file
):

    files = {

        "file": (

            uploaded_file.name,

            uploaded_file,

            "text/csv"
        )
    }

    response = requests.post(

        f"{API_URL}/batch_predict_csv",

        files=files,

        timeout=800
    )

    response.raise_for_status()

    return response.content