def compute_dashboard_metrics(df):

    metrics = {

        "total_shipments": len(df),

        "critical_count": (
            df["Risk_Label"]
            == "Critical"
        ).sum(),

        "medium_count": (
            df["Risk_Label"]
            == "Medium"
        ).sum(),

        "low_count": (
            df["Risk_Label"]
            == "Low"
        ).sum(),

        "avg_anomaly_score": (
            df["Anomaly_Score"]
            .mean()
        ),

        "avg_dwell_time": (
            df["Dwell_Time_Hours"]
            .mean()
        )
    }

    return metrics