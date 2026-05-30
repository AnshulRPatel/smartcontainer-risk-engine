import os

import pandas as pd

from uuid import uuid4

from typing import List

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import (
    FileResponse
)

from app.models.schemas import (

    ShipmentInput,

    PredictionResponse,

    BatchPredictionResponse
)

from app.services.model_service import (
    model_service
)


router = APIRouter()


# =====================================================
# SINGLE PREDICTION
# =====================================================

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

        "container_id":
        shipment.Container_ID,

        "predicted_risk":
        result[
            "predicted_risk"
        ],

        "risk_label":
        result[
            "risk_label"
        ],

        "model_confidence":
        result[
            "model_confidence"
        ],

        "risk_score":
        result[
            "risk_score"
        ],

        "anomaly_score":
        result[
            "anomaly_score"
        ],

        "explanation":
        result[
            "explanation"
        ]
    }


# =====================================================
# JSON BATCH PREDICTION
# =====================================================

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


# =====================================================
# CSV BATCH PREDICTION
# =====================================================

@router.post(
    "/batch_predict_csv"
)
def batch_predict_csv(

    file: UploadFile = File(...)
):

    # ==========================================
    # VALIDATE FILE
    # ==========================================

    if not file.filename:

        raise HTTPException(

            status_code=400,

            detail=
            "No file uploaded."
        )

    if not file.filename.lower().endswith(
        ".csv"
    ):

        raise HTTPException(

            status_code=400,

            detail=
            "Only CSV files are supported."
        )

    # ==========================================
    # LOAD CSV
    # ==========================================

    try:

        df = pd.read_csv(
            file.file
        )

        print("\n========== CSV COLUMNS ==========\n")
        print(df.columns.tolist())

        # ==========================================
        # NORMALIZE TEMPLATE COLUMN NAMES
        # ==========================================

        df = df.rename(
            columns={

                "Declaration_Date (YYYY-MM-DD)":
                "Declaration_Date",

                "Trade_Regime (Import / Export / Transit)":
                "Trade_Regime"
            }
        )

        required_columns = [

            "Container_ID",

            "Declaration_Date",

            "Declaration_Time",

            "Trade_Regime",

            "Origin_Country",

            "Destination_Port",

            "Destination_Country",

            "HS_Code",

            "Importer_ID",

            "Exporter_ID",

            "Declared_Value",

            "Declared_Weight",

            "Measured_Weight",

            "Shipping_Line",

            "Dwell_Time_Hours"
        ]

        missing_columns = [

            col

            for col in required_columns

            if col not in df.columns
        ]

        if missing_columns:

            raise HTTPException(

                status_code=400,

                detail=
                f"Missing required columns: {missing_columns}"
            )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=
            f"Invalid CSV file: {str(e)}"
        )

    # ==========================================
    # CONVERT TO SHIPMENT RECORDS
    # ==========================================

    shipments = (

        df.to_dict(
            orient="records"
        )
    )

    # ==========================================
    # BATCH PREDICTION
    # ==========================================

    results = (

        model_service
        .batch_predict(
            shipments
        )
    )

    # ==========================================
    # BUILD OUTPUT DATASET
    # ==========================================

    output_rows = []

    for shipment, result in zip(

        shipments,

        results
    ):

        output_rows.append({

            **shipment,

            **result
        })

    output_df = pd.DataFrame(
        output_rows
    )

    # ==========================================
    # CREATE OUTPUT DIRECTORY
    # ==========================================

    os.makedirs(

        "outputs/predictions",

        exist_ok=True
    )

    # ==========================================
    # SAVE OUTPUT FILE
    # ==========================================

    file_id = (
        uuid4().hex
    )

    output_path = (

        f"outputs/predictions/"
        f"predictions_"
        f"{file_id}.csv"
    )

    output_df.to_csv(

        output_path,

        index=False
    )

    # ==========================================
    # RETURN FILE
    # ==========================================

    return FileResponse(

        path=output_path,

        filename=
        f"predictions_"
        f"{file_id[:8]}.csv",

        media_type=
        "text/csv"
    )