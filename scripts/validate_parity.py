import pandas as pd

from pathlib import Path

from app.services.model_service import (
    model_service
)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "data/processed/anomaly_shipments.csv"
)

results = []

# ==========================================
# VALIDATE ALL CONTAINERS
# ==========================================

for _, row in df.iterrows():

    shipment = {

        "Container_ID":
        str(row["Container_ID"]),

        "Declared_Value":
        float(row["Declared_Value"]),

        "Declared_Weight":
        float(row["Declared_Weight"]),

        "Measured_Weight":
        float(row["Measured_Weight"]),

        "Dwell_Time_Hours":
        float(row["Dwell_Time_Hours"]),

        "Trade_Regime":
        row["Trade_Regime"],

        "Origin_Country":
        row["Origin_Country"],

        "Destination_Country":
        row["Destination_Country"],

        "Destination_Port":
        row["Destination_Port"],

        "Shipping_Line":
        row["Shipping_Line"],

        "HS_Code":
        str(row["HS_Code"]),

        "Declaration_Date":
        str(row["Declaration_Date"]),

        "Declaration_Time":
        str(row["Declaration_Time"]),

        "Importer_ID":
        row["Importer_ID"],

        "Exporter_ID":
        row["Exporter_ID"]
    }

    try:

        result = (
            model_service.predict(
                shipment
            )
        )

        match = (

            row["Risk_Label"]
            ==
            result["risk_label"]
        )

        results.append({

            "Container_ID":
            row["Container_ID"],

            "Training_Label":
            row["Risk_Label"],

            "API_Risk_Label":
            result["risk_label"],

            "Match":
            match,

            "Predicted_Risk":
            result["predicted_risk"],

            "Training_Score":
            round(
                float(
                    row["Total_Risk_Score"]
                ),
                6
            ),

            "API_Score":
            round(
                float(
                    result["risk_score"]
                ),
                6
            ),

            "Training_Anomaly":
            round(
                float(
                    row["Anomaly_Score"]
                ),
                6
            ),

            "API_Anomaly":
            round(
                float(
                    result["anomaly_score"]
                ),
                6
            ),

            "Model_Confidence":
            result["model_confidence"]
        })

    except Exception as e:

        results.append({

            "Container_ID":
            row["Container_ID"],

            "Training_Label":
            row["Risk_Label"],

            "API_Risk_Label":
            "ERROR",

            "Match":
            False,

            "Predicted_Risk":
            "ERROR",

            "Training_Score":
            row["Total_Risk_Score"],

            "API_Score":
            None,

            "Training_Anomaly":
            row["Anomaly_Score"],

            "API_Anomaly":
            None,

            "Model_Confidence":
            None
        })

# ==========================================
# SAVE CSV REPORT
# ==========================================

report_df = pd.DataFrame(
    results
)

output_dir = Path(
    "outputs/reports"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

report_path = (
    output_dir
    /
    "train_api_parity_validation.csv"
)

report_df.to_csv(

    report_path,

    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("\n===================================")
print("TRAIN/API PARITY VALIDATION")
print("===================================")

print(
    f"Total Rows: {len(report_df)}"
)

print(
    f"Matches: {report_df['Match'].sum()}"
)

print(
    f"Mismatches: {len(report_df) - report_df['Match'].sum()}"
)

print(
    f"\nSaved:\n{report_path}"
)