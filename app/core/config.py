from functools import lru_cache

from pydantic_settings import (
    BaseSettings
)


class Settings(BaseSettings):

    app_name: str = (
        "SmartContainer Risk Engine"
    )

    environment: str = (
        "development"
    )

    api_version: str = (
        "v1"
    )

    model_path: str = (
        "outputs/models/catboost_risk_model.cbm"
    )

    allowed_origins: list[str] = [
        "*"
    ]

    class Config:

        env_file = ".env"


@lru_cache
def get_settings():

    return Settings()