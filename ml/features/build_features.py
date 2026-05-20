import pandas as pd

from ml.features.anomaly_features import (
    add_weight_discrepancy_features,
    add_value_density_features,
    add_log_transforms,
    add_hs_code_features,
    add_dwell_time_flags
)

from ml.features.behavioral_features import (
    add_importer_risk_features,
    add_exporter_risk_features,
    add_shipping_line_frequency
)

from ml.features.temporal_features import (
    add_date_features,
    add_time_features
)

from ml.features.outlier_features import (
    winsorize_columns
)

def build_feature_pipeline(df):

    df = add_weight_discrepancy_features(df)

    df = add_value_density_features(df)

    df = add_log_transforms(df)

    df = add_hs_code_features(df)

    df = add_dwell_time_flags(df)

    df = add_importer_risk_features(df)

    df = add_exporter_risk_features(df)

    df = add_shipping_line_frequency(df)

    df = add_date_features(df)

    df = add_time_features(df)

    df = winsorize_columns(
        df,
        cols=[
            "Declared_Value",
            "Declared_Weight",
            "Measured_Weight",
            "Value_Per_Weight",
            "Weight_Difference"
        ]
    )

    return df


if __name__ == "__main__":

    df = pd.read_csv(
        "data/processed/cleaned_shipments.csv",
        parse_dates=["Declaration_Date"]
    )

    df = build_feature_pipeline(df)

    df.to_csv(
        "data/processed/featured_shipments.csv",
        index=False
    )

    print("Feature engineering complete.")