import pandas as pd

from ml.preprocessing.schema import (
    EXPECTED_COLUMNS,
    VALID_TRADE_REGIMES,
    VALID_CLEARANCE_STATUS
)

def validate_columns(df: pd.DataFrame):
    missing = set(EXPECTED_COLUMNS.keys()) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

def validate_trade_regime(df):
    invalid = df[
        ~df["Trade_Regime"].isin(VALID_TRADE_REGIMES)
    ]

    return invalid

def validate_clearance_status(df):
    invalid = df[
        ~df["Clearance_Status"].isin(VALID_CLEARANCE_STATUS)
    ]

    return invalid