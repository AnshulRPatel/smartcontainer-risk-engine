import pandas as pd


def classify_value_risk(
    value,
    q95,
    q99
):

    if value >= q99:

        return (
            "extremely high cargo value"
        )

    elif value >= q95:

        return (
            "high cargo value"
        )

    return None


def classify_weight_risk(
    pct
):

    abs_pct = abs(pct)

    if abs_pct > 50:

        return (
            "severe weight discrepancy"
        )

    elif abs_pct > 20:

        return (
            "abnormal weight discrepancy"
        )

    return None


def classify_dwell_risk(
    dwell_hours,
    threshold
):

    if dwell_hours > threshold * 1.5:

        return (
            "extreme port dwell duration"
        )

    elif dwell_hours > threshold:

        return (
            "excessive dwell time"
        )

    return None


def classify_behavioral_risk(
    shipment_count,
    threshold
):

    if shipment_count < threshold:

        return (
            "limited importer shipment history"
        )

    return None


def build_explanation(

    row,

    q95_value,

    q99_value,

    dwell_threshold,

    importer_threshold
):

    reasons = []

    # =========================
    # ANOMALY SCORE
    # =========================

    if row["Anomaly_Score"] < 0:

        reasons.append(
            "high anomaly score"
        )

    # =========================
    # VALUE RISK
    # =========================

    value_reason = classify_value_risk(

        row["Declared_Value"],

        q95_value,

        q99_value
    )

    if value_reason:

        reasons.append(value_reason)

    # =========================
    # WEIGHT RISK
    # =========================

    weight_reason = classify_weight_risk(

        row["Weight_Difference_Percent"]
    )

    if weight_reason:

        reasons.append(weight_reason)

    # =========================
    # DWELL RISK
    # =========================

    dwell_reason = classify_dwell_risk(

        row["Dwell_Time_Hours"],

        dwell_threshold
    )

    if dwell_reason:

        reasons.append(dwell_reason)

    # =========================
    # TEMPORAL RISK
    # =========================

    if row["Is_Night_Declaration"] == 1:

        reasons.append(
            "night-time declaration activity"
        )

    # =========================
    # BEHAVIORAL RISK
    # =========================

    behavioral_reason = (

        classify_behavioral_risk(

            row[
                "Importer_Shipment_Count"
            ],

            importer_threshold
        )
    )

    if behavioral_reason:

        reasons.append(
            behavioral_reason
        )

    # =========================
    # LOW-RISK SHIPMENTS
    # =========================

    if len(reasons) == 0:

        return (
            "Shipment characteristics align "
            "with normal operational and "
            "behavioral patterns."
        )

    # =========================
    # PRIORITIZE TOP SIGNALS
    # =========================

    reasons = reasons[:3]

    # =========================
    # RISK-SPECIFIC LANGUAGE
    # =========================

    if row["Risk_Label"] == "Critical":

        prefix = (
            "Container classified as "
            "Critical Risk due to "
        )

    elif row["Risk_Label"] == "Medium":

        prefix = (
            "Container flagged for "
            "moderate operational risk due to "
        )

    else:

        prefix = (
            "Container monitored due to "
        )

    explanation = (
        prefix
        + ", ".join(reasons)
        + "."
    )

    return explanation


def generate_explanation_summary(df):

    print(
        "Generating operational explanations..."
    )

    # =========================
    # DYNAMIC THRESHOLDS
    # =========================

    q95_value = (
        df["Declared_Value"]
        .quantile(0.95)
    )

    q99_value = (
        df["Declared_Value"]
        .quantile(0.99)
    )

    dwell_threshold = (
        df["Dwell_Time_Hours"]
        .quantile(0.95)
    )

    importer_threshold = (
        df["Importer_Shipment_Count"]
        .quantile(0.10)
    )

    df["Explanation_Summary"] = (

        df.apply(

            lambda row:

            build_explanation(

                row,

                q95_value,

                q99_value,

                dwell_threshold,

                importer_threshold
            ),

            axis=1
        )
    )

    return df


if __name__ == "__main__":

    print(
        "Loading anomaly shipment dataset..."
    )

    df = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

    df = generate_explanation_summary(df)

    output_cols = [

        "Container_ID",

        "Risk_Label",

        "Total_Risk_Score",

        "Anomaly_Score",

        "Explanation_Summary"
    ]

    df[output_cols].to_csv(

        "outputs/reports/prediction_explanations.csv",

        index=False
    )

    print(
        "\nExplanation generation complete."
    )