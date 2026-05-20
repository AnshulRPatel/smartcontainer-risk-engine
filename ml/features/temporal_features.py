def add_date_features(df):

    df["Declaration_Year"] = (
        df["Declaration_Date"].dt.year
    )

    df["Declaration_Month"] = (
        df["Declaration_Date"].dt.month
    )

    df["Declaration_Day"] = (
        df["Declaration_Date"].dt.day
    )

    df["Declaration_Weekday"] = (
        df["Declaration_Date"].dt.weekday
    )

    return df

import pandas as pd
def add_time_features(df):

    parsed = pd.to_datetime(
        df["Declaration_Time"],
        format="%H:%M:%S",
        errors="coerce"
    )

    df["Declaration_Hour"] = parsed.dt.hour

    df["Is_Business_Hours"] = (
        df["Declaration_Hour"]
        .between(8, 18)
    ).astype(int)

    df["Is_Night_Declaration"] = (
        ~df["Declaration_Hour"]
        .between(6, 22)
    ).astype(int)

    return df