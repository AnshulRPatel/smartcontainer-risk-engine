from fastapi import APIRouter

from ml.modeling.preprocess import (
    FEATURE_COLUMNS
)

from app.core.version import (
    MODEL_NAME,
    MODEL_VERSION,
    API_VERSION
)

from app.models.schemas import (
    ModelInfoResponse
)


router = APIRouter()


@router.get(
    "/model_info",
    response_model=ModelInfoResponse
)
def get_model_info():

    return {

        "model_name":
        MODEL_NAME,

        "model_version":
        MODEL_VERSION,

        "api_version":
        API_VERSION,

        "framework":
        "CatBoost",

        "task":
        "Customs Risk Classification",

        "target_classes":
        [
            "Critical",
            "Medium",
            "Low"
        ],

        "features_count":
        len(
            FEATURE_COLUMNS
        ),

        "features":
        FEATURE_COLUMNS
    }