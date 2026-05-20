import pandas as pd

from ml.anomaly_detection.isolation_forest import (
    train_isolation_forest
)


ANOMALY_FEATURES = [

    "Weight_Difference_Percent",

    "Value_Per_Weight",

    "Dwell_Time_Hours",

    "Importer_Shipment_Count",

    "Exporter_Shipment_Count",

    "Shipping_Line_Frequency",

    "Declaration_Hour",

    "was_zero_declared_weight",

    "was_zero_declared_value",

    "Log_Declared_Value",

    "Log_Declared_Weight"
]


def build_anomaly_pipeline(df):

    df, model = train_isolation_forest(
        df,
        ANOMALY_FEATURES
    )

    return df, model


if __name__ == "__main__":

    print("Loading labeled shipment dataset...")

    df = pd.read_csv(
        "data/processed/labeled_shipments.csv"
    )

    print(f"Dataset Shape: {df.shape}")

    df, model = build_anomaly_pipeline(df)

    print("\nAnomaly Flag Distribution:\n")

    print(
        df["Anomaly_Flag"]
        .value_counts()
    )

    print("\nCross-tabulation with Risk Labels:\n")

    print(
        pd.crosstab(
            df["Risk_Label"],
            df["Anomaly_Flag"]
        )
    )

    df.to_csv(
        "data/processed/anomaly_shipments.csv",
        index=False
    )

    print("\nAnomaly detection complete.")