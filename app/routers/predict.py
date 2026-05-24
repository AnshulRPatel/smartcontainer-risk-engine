from fastapi import APIRouter

from app.models.schemas import (

    ShipmentInput,

    PredictionResponse
)

from app.services.model_service import (
    model_service
)


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
            shipment.dict()
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