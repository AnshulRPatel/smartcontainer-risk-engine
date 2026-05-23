import streamlit as st


def render_critical_queue(df):

    st.subheader(
        "Critical Shipment Queue"
    )

    critical_df = (

        df[
            df["Risk_Label"]
            == "Critical"
        ]

        .sort_values(
            "Total_Risk_Score",
            ascending=False
        )
    )

    display_cols = [

        "Container_ID",

        "Risk_Label",

        "Total_Risk_Score",

        "Anomaly_Score",

        "Declared_Value",

        "Dwell_Time_Hours",

        "Explanation_Summary"
    ]

    st.dataframe(
        critical_df[display_cols]
    )