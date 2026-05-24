from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.core.config import (
    get_settings
)

from app.core.logging import (
    configure_logging
)

from app.routers import (

    health,

    predict
)

from app.routers import (
    model_info
)

settings = get_settings()

configure_logging()

app = FastAPI(

    title=(
        "SmartContainer Risk Engine"
    ),

    version="1.0.0"
)


@app.get("/")
def root():

    return {

        "message": (
            "SmartContainer "
            "Risk Engine API"
        ),

        "docs": "/docs"
    }

app.add_middleware(

    CORSMiddleware,

    allow_origins=(
        settings.allowed_origins
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(
    health.router
)

app.include_router(
    predict.router
)

app.include_router(
    model_info.router
)