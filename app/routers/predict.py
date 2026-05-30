from fastapi import APIRouter

from app.models.schemas import (

    ShipmentInput,

    PredictionResponse,

    BatchPredictionResponse
)

from app.services.model_service import (
    model_service
)

from typing import List

router = APIRouter()


@router.post(

    "/predict",

    response_model=PredictionResponse
)
def predict_risk(

    shipment: ShipmentInput
):

    result = (

        model_service.predict(
            shipment.model_dump()
        )
    )

    return {

    "container_id": (
        shipment.Container_ID
    ),

    "predicted_risk": (
        result[
            "predicted_risk"
        ]
    ),

    "risk_label": (
        result[
            "risk_label"
        ]
    ),

    "model_confidence": (
        result[
            "model_confidence"
        ]
    ),

    "risk_score": (
        result[
            "risk_score"
        ]
    ),

    "anomaly_score": (
        result[
            "anomaly_score"
        ]
    ),

    "explanation": (
        result[
            "explanation"
        ]
    )
}

@router.post(

    "/batch_predict",

    response_model=
    List[
        BatchPredictionResponse
    ]
)
def batch_predict_risk(

    shipments:
    List[
        ShipmentInput
    ]
):

    shipment_dicts = [

        shipment.model_dump()

        for shipment

        in shipments
    ]

    results = (

        model_service
        .batch_predict(

            shipment_dicts
        )
    )

    response = []

    for shipment, result in zip(

        shipments,

        results
    ):

        response.append({

            "container_id":
            shipment.Container_ID,

            **result
        })

    return response