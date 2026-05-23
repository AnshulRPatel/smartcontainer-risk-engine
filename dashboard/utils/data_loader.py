import pandas as pd

import streamlit as st


@st.cache_data
def load_dashboard_data():

    shipments = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

    explanations = pd.read_csv(
        "outputs/reports/prediction_explanations.csv"
    )

    merged = shipments.merge(

        explanations[
            [
                "Container_ID",
                "Explanation_Summary"
            ]
        ],

        on="Container_ID",

        how="left"
    )

    return merged