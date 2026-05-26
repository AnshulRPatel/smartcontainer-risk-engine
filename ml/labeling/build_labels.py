import pandas as pd

from ml.labeling.heuristic_rules import (
    add_weight_risk,
    add_value_risk,
    add_dwell_risk,
    add_behavioral_risk,
    add_temporal_risk,
    add_data_integrity_risk,
    add_route_risk
)

from ml.labeling.risk_scoring import (
    compute_total_risk_score
)

from ml.labeling.pseudo_labels import (
    generate_pseudo_labels
)

from ml.labeling.save_thresholds import (
    save_risk_thresholds
)

def build_label_pipeline(df):

    print("Applying weight risk scoring...")
    df = add_weight_risk(df)

    print("Applying value risk scoring...")
    df = add_value_risk(df)

    print("Applying dwell-time risk scoring...")
    df = add_dwell_risk(df)

    print("Applying behavioral risk scoring...")
    df = add_behavioral_risk(df)

    print("Applying temporal risk scoring...")
    df = add_temporal_risk(df)

    print("Applying data integrity risk scoring...")
    df = add_data_integrity_risk(df)

    print("Applying route risk scoring...")
    df = add_route_risk(df)

    # =====================================================
    # SAVE TRAINING THRESHOLDS
    # =====================================================

    value_threshold_95 = (
        df["Declared_Value"]
        .quantile(0.95)
    )

    value_threshold_99 = (
        df["Declared_Value"]
        .quantile(0.99)
    )

    dwell_threshold_95 = (
        df["Dwell_Time_Hours"]
        .quantile(0.95)
    )

    importer_threshold_10 = (
        df["Importer_Shipment_Count"]
        .quantile(0.10)
    )

    save_risk_thresholds(

        value_threshold_95,

        value_threshold_99,

        dwell_threshold_95,

        importer_threshold_10
    )

    print("Computing hybrid weighted risk score...")
    df = compute_total_risk_score(df)

    print("Generating pseudo labels...")
    df = generate_pseudo_labels(df)

    return df


if __name__ == "__main__":

    print("Loading featured shipment dataset...")

    df = pd.read_csv(
        "data/processed/featured_shipments.csv"
    )

    print(f"Dataset Shape: {df.shape}")

    df = build_label_pipeline(df)

    print("\nRisk Label Distribution:\n")

    print(
        df["Risk_Label"]
        .value_counts()
    )

    print("\nSaving labeled dataset...")

    df.to_csv(
        "data/processed/labeled_shipments.csv",
        index=False
    )

    print("\nRisk label generation complete.")