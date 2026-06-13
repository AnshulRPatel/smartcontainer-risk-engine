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

from app.services.monitoring_service import (
    monitoring_service
)


from app.services.schema_service import (
    schema_service
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

    monitoring_service.log_prediction(

    shipment.Container_ID,

    result
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

        monitoring_service.log_prediction(

        shipment.Container_ID,

        result
        )

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
        # APPLY SCHEMA VALIDATION PIPELINE
        # ==========================================

        validation_result = (

            schema_service
            .validate_and_clean(df)
        )

        df = validation_result[
            "clean_df"
        ]

        removed_rows = validation_result[
            "removed_rows"
        ]

        
        failed_df = validation_result[
            "failed_df"
        ]


        print(
            f"\nRemoved invalid rows: "
            f"{removed_rows}"
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

        monitoring_service.log_prediction(

        shipment[
            "Container_ID"
        ],

        result
    )

        output_rows.append({

            **shipment,

            **result
        })

    output_df = pd.DataFrame(
        output_rows
    )

    
    # ==========================================
    # INGESTION METRICS
    # ==========================================

    total_uploaded_rows = (

        len(df) + removed_rows
    )

    successful_rows = len(df)

    failed_rows_count = removed_rows

    success_rate = round(

        (successful_rows / total_uploaded_rows)
        * 100,

        2
    )
    
    # ==========================================
    # SAVE FAILED ROWS REPORT
    # ==========================================

    os.makedirs(

        "outputs/errors",

        exist_ok=True
    )

    error_file_id = (
        uuid4().hex
    )

    error_output_path = (

        f"outputs/errors/"
        f"failed_rows_"
        f"{error_file_id}.csv"
    )

    failed_df.to_csv(

        error_output_path,

        index=False
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

    output_df[
        "Total_Uploaded_Rows"
    ] = total_uploaded_rows

    output_df[
        "Successful_Rows"
    ] = successful_rows

    output_df[
        "Failed_Rows"
    ] = failed_rows_count

    output_df[
        "Success_Rate_Percent"
    ] = success_rate
    
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

@router.get(
    "/download_template"
)
def download_template():

    template_path = (
        "templates/"
        "shipment_template.csv"
    )

    return FileResponse(

        path=template_path,

        filename=
        "shipment_template.csv",

        media_type=
        "text/csv"
    )