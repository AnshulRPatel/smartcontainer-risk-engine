import pandas as pd


def evaluate_anomaly_alignment(df):

    print("\n========== CROSS-TABULATION ==========\n")

    cross_tab = pd.crosstab(
        df["Risk_Label"],
        df["Anomaly_Flag"]
    )

    print(cross_tab)

    print("\n========== ANOMALY RATE BY RISK LABEL ==========\n")

    anomaly_rates = (
        df.groupby("Risk_Label")["Anomaly_Flag"]
        .mean()
        .sort_values(ascending=False)
    )

    print(anomaly_rates)

    print("\n========== AVERAGE ANOMALY SCORE ==========\n")

    avg_scores = (
        df.groupby("Risk_Label")["Anomaly_Score"]
        .mean()
        .sort_values()
    )

    print(avg_scores)

    print("\n========== CRITICAL-CLASS ANOMALY PRECISION ==========\n")

    critical_precision = (
        (
            (df["Risk_Label"] == "Critical")
            &
            (df["Anomaly_Flag"] == 1)
        ).sum()
        /
        (df["Anomaly_Flag"] == 1).sum()
    )

    print(
        f"Precision: {critical_precision:.4f}"
    )

    print("\n========== TOP 10 MOST ANOMALOUS SHIPMENTS ==========\n")

    top_anomalies = (
        df.sort_values("Anomaly_Score")
        .head(10)
        [
            [
                "Container_ID",
                "Risk_Label",
                "Anomaly_Score",
                "Weight_Difference_Percent",
                "Value_Per_Weight",
                "Dwell_Time_Hours",
                "Origin_Country",
                "Destination_Port"
            ]
        ]
    )

    print(top_anomalies)

    print("\n========== ANOMALY SCORE SUMMARY ==========\n")

    print(
        df["Anomaly_Score"]
        .describe()
    )


if __name__ == "__main__":

    print("Loading anomaly shipment dataset...")

    df = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

    print(f"Dataset Shape: {df.shape}")

    evaluate_anomaly_alignment(df)