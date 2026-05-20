import numpy as np


def add_weight_risk(df):

    df["Weight_Risk_Score"] = np.select(
        [
            abs(df["Weight_Difference_Percent"]) > 50,
            abs(df["Weight_Difference_Percent"]) > 20
        ],
        [3, 2],
        default=0
    )

    return df


def add_value_risk(df):

    threshold_99 = (
        df["Declared_Value"]
        .quantile(0.99)
    )

    threshold_95 = (
        df["Declared_Value"]
        .quantile(0.95)
    )

    df["Value_Risk_Score"] = np.select(
        [
            df["Declared_Value"] > threshold_99,
            df["Declared_Value"] > threshold_95
        ],
        [3, 2],
        default=0
    )

    return df


def add_dwell_risk(df):

    threshold = (
        df["Dwell_Time_Hours"]
        .quantile(0.95)
    )

    df["Dwell_Risk_Score"] = (
        df["Dwell_Time_Hours"] > threshold
    ).astype(int) * 2

    return df


def add_behavioral_risk(df):

    low_importer_threshold = (
        df["Importer_Shipment_Count"]
        .quantile(0.10)
    )

    df["Behavioral_Risk_Score"] = (
        df["Importer_Shipment_Count"]
        < low_importer_threshold
    ).astype(int) * 3

    return df

def add_temporal_risk(df):

    df["Temporal_Risk_Score"] = (
        df["Is_Night_Declaration"]
    ).astype(int) * 2

    return df

def add_data_integrity_risk(df):

    df["Integrity_Risk_Score"] = (
        (
            df["was_zero_declared_weight"]
            +
            df["was_zero_declared_value"]
        ) > 0
    ).astype(int) * 3

    return df

def add_route_risk(df):

    route_counts = (
        df.groupby(
            [
                "Origin_Country",
                "Destination_Port"
            ]
        )
        .size()
    )

    rare_threshold = (
        route_counts.quantile(0.10)
    )

    rare_routes = route_counts[
        route_counts < rare_threshold
    ].index

    df["Route_Risk_Score"] = df.apply(
        lambda row:
        2 if (
            row["Origin_Country"],
            row["Destination_Port"]
        ) in rare_routes
        else 0,
        axis=1
    )

    return df