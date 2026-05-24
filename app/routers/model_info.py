from fastapi import APIRouter


router = APIRouter()


@router.get("/model_info")
def model_info():

    return {

        "model_name": (
            "CatBoost Risk Model"
        ),

        "model_version": "1.0",

        "framework": "CatBoost",

        "task": (
            "Customs Risk Classification"
        )
    }