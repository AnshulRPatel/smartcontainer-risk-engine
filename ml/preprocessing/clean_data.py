import pandas as pd

from ml.preprocessing.validators import (
    validate_columns
)

from ml.preprocessing.schema import EXPECTED_COLUMNS


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def standardize_column_names(df):

    # Explicit mapping from raw dataset columns
    # to internal ML pipeline schema
    COLUMN_MAPPING = {
        "Declaration_Date (YYYY-MM-DD)": "Declaration_Date",
        "Trade_Regime (Import / Export / Transit)": "Trade_Regime",
    }

    df = df.rename(columns=COLUMN_MAPPING)

    # General cleanup
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )

    return df


def convert_dtypes(df):

    for col, dtype in EXPECTED_COLUMNS.items():

        if col not in df.columns:
            continue

        if "datetime" in dtype:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

        else:
            try:
                df[col] = df[col].astype(dtype)

            except Exception:
                pass

    return df


def remove_duplicates(df):
    return df.drop_duplicates()


def handle_missing_values(df):

    numeric_cols = df.select_dtypes(
        include=["float64", "int64"]
    ).columns

    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    return df


def clean_pipeline(path):

    print("Loading dataset...")

    df = load_dataset(path)

    print("Original Columns:")
    print(df.columns.tolist())

    df = standardize_column_names(df)

    print("\nStandardized Columns:")
    print(df.columns.tolist())

    validate_columns(df)

    df = convert_dtypes(df)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    print("\nDataset Shape:", df.shape)

    return df


if __name__ == "__main__":

    df = clean_pipeline(
        "data/raw/container_shipments.csv"
    )

    df.to_csv(
        "data/processed/cleaned_shipments.csv",
        index=False
    )

    print("\nData cleaning complete.")