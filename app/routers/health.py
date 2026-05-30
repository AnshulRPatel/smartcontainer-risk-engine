from datetime import (
    datetime,
    timezone
)

from fastapi import APIRouter

from app.services.model_service import (
    model_service
)

from app.core.version import (
    API_VERSION,
    MODEL_NAME
)

from app.models.schemas import (
    HealthResponse,
    ReadyResponse
)


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return {

        "status":
        "healthy",

        "service":
        MODEL_NAME,

        "api_version":
        API_VERSION,

        "timestamp":
        datetime
        .now(
            timezone.utc
        )
        .isoformat(),

        "model_loaded":
        (
            model_service.model
            is not None
        )
    }


@router.get(
    "/ready",
    response_model=ReadyResponse
)
def readiness_check():

    return {

        "ready":
        (
            model_service.model
            is not None
        )
    }