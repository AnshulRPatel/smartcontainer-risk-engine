from fastapi import APIRouter

from app.models.schemas import (

    ShipmentInput,

    ExplanationResponse
)

from app.services.model_service import (
    model_service
)

from app.services.explainability_api_service import (
    explainability_api_service
)


router = APIRouter()


@router.post(

    "/explain",

    response_model=
    ExplanationResponse
)
def explain_prediction(

    shipment: ShipmentInput
):

    result = (
        model_service.explain(
            shipment.model_dump()
        )
    )

    prediction = (
        result[
            "prediction"
        ]
    )

    processed_df = (
        result[
            "processed_df"
        ]
    )

    factors = (

        explainability_api_service
        .extract_risk_factors(

            prediction,

            processed_df
        )
    )

    return {

        "container_id":
        shipment.Container_ID,

        **prediction,

        "top_risk_factors":
        factors
    }