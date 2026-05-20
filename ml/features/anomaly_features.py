import numpy as np


def add_weight_discrepancy_features(df):

    

    df["Weight_Difference"] = (
        df["Measured_Weight"]
        - df["Declared_Weight"]
    )

    df["Weight_Difference_Percent"] = np.where(
        df["Declared_Weight"] > 0,
        (
            df["Weight_Difference"]
            / df["Declared_Weight"]
        ) * 100,
        np.nan
    )

    df["High_Weight_Anomaly"] = (
        abs(df["Weight_Difference_Percent"]) > 20
    ).astype(int)

    return df


def add_value_density_features(df):

    df["Value_Per_Weight"] = (
        df["Declared_Value"]
        / (df["Declared_Weight"] + 1e-6)
    )

    return df

def add_hs_code_features(df):

    df["HS_Code"] = (
        df["HS_Code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(6)
    )

    df["HS_Chapter"] = (
        df["HS_Code"].str[:2]
    )

    df["HS_Heading"] = (
        df["HS_Code"].str[:4]
    )

    return df


def add_log_transforms(df):

    

    df["Log_Declared_Value"] = np.log1p(
        df["Declared_Value"]
    )

    df["Log_Declared_Weight"] = np.log1p(
        df["Declared_Weight"]
    )

    return df


def add_dwell_time_flags(df):

    threshold = df["Dwell_Time_Hours"].quantile(0.95)

    df["Excessive_Dwell_Flag"] = (
        df["Dwell_Time_Hours"] > threshold
    ).astype(int)

    return df