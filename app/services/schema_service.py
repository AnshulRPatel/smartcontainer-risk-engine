import re

import pandas as pd


class SchemaService:

    def __init__(self):

        # =========================================
        # REQUIRED MODEL INPUT COLUMNS
        # =========================================

        self.required_columns = [

            "Container_ID",

            "Declaration_Date",

            "Declaration_Time",

            "Trade_Regime",

            "Origin_Country",

            "Destination_Port",

            "Destination_Country",

            "HS_Code",

            "Importer_ID",

            "Exporter_ID",

            "Declared_Value",

            "Declared_Weight",

            "Measured_Weight",

            "Shipping_Line",

            "Dwell_Time_Hours"
        ]

        # =========================================
        # COLUMN ALIAS MAP
        # =========================================

        self.column_aliases = {

            "containerid":
            "Container_ID",

            "container_id":
            "Container_ID",

            "declaredvalue":
            "Declared_Value",

            "declared_value":
            "Declared_Value",

            "declared weight":
            "Declared_Weight",

            "measuredweight":
            "Measured_Weight",

            "shippingline":
            "Shipping_Line",

            "dwelltimehours":
            "Dwell_Time_Hours",

            "origincountry":
            "Origin_Country",

            "destinationcountry":
            "Destination_Country",

            "destinationport":
            "Destination_Port",

            "importerid":
            "Importer_ID",

            "exporterid":
            "Exporter_ID",

            "hscode":
            "HS_Code"
        }

    # =============================================
    # NORMALIZE COLUMN NAME
    # =============================================

    def normalize_column_name(

        self,

        column
    ):

        normalized = (

            column
            .strip()
            .lower()
        )

        normalized = re.sub(

            r"[^a-z0-9]",

            "",

            normalized
        )

        return self.column_aliases.get(

            normalized,

            column
        )

    # =============================================
    # NORMALIZE ALL COLUMNS
    # =============================================

    def normalize_columns(

        self,

        df
    ):

        df.columns = [

            self.normalize_column_name(
                col
            )

            for col in df.columns
        ]

        return df

    # =============================================
    # VALIDATE REQUIRED COLUMNS
    # =============================================

    def validate_required_columns(

        self,

        df
    ):

        missing_columns = [

            col

            for col in self.required_columns

            if col not in df.columns
        ]

        if missing_columns:

            raise ValueError(

                f"Missing required columns: "
                f"{missing_columns}"
            )

    # =============================================
    # SAFE TYPE CONVERSION
    # =============================================

    def clean_numeric_column(

        self,

        series
    ):

        return pd.to_numeric(

            series.astype(str)

            .str.replace(",", ""),

            errors="coerce"
        )

    # =============================================
    # APPLY DATA CLEANING
    # =============================================

    def clean_dataframe(

        self,

        df
    ):

        numeric_columns = [

            "Declared_Value",

            "Declared_Weight",

            "Measured_Weight",

            "Dwell_Time_Hours"
        ]

        for col in numeric_columns:

            if col in df.columns:

                df[col] = (
                    self.clean_numeric_column(
                        df[col]
                    )
                )

        return df

    # =============================================
    # REMOVE INVALID ROWS
    # =============================================

    
    def remove_invalid_rows(

        self,

        df
    ):

        failed_rows = []

        valid_rows = []

        required_numeric_columns = [

            "Declared_Value",

            "Declared_Weight",

            "Measured_Weight"
        ]

        for _, row in df.iterrows():

            row_errors = []

            for col in required_numeric_columns:

                if pd.isna(row[col]):

                    row_errors.append(
                        f"Missing or invalid {col}"
                    )

            if row_errors:

                failed_row = row.to_dict()

                failed_row[
                    "Error_Reason"
                ] = "; ".join(row_errors)

                failed_rows.append(
                    failed_row
                )

            else:

                valid_rows.append(
                    row.to_dict()
                )

        clean_df = pd.DataFrame(
            valid_rows
        )

        failed_df = pd.DataFrame(
            failed_rows
        )

        return {

            "clean_df":
            clean_df,

            "failed_df":
            failed_df,

            "removed_rows":
            len(failed_rows)
        }
    


    # =============================================
    # FULL VALIDATION PIPELINE
    # =============================================

    def validate_and_clean(

        self,

        df
    ):

        df = self.normalize_columns(
            df
        )

        self.validate_required_columns(
            df
        )

        df = self.clean_dataframe(
            df
        )

        
        row_validation_result = (

            self.remove_invalid_rows(df)
        )

        df = row_validation_result[
            "clean_df"
        ]

        failed_df = row_validation_result[
            "failed_df"
        ]

        removed_rows = row_validation_result[
            "removed_rows"
        ]
        
        return {

            "clean_df": df,

            "failed_df": failed_df,

            "removed_rows":
            removed_rows
        }

schema_service = SchemaService()