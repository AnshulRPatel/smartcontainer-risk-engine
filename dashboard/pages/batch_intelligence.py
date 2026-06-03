import io

import pandas as pd

import plotly.express as px

import streamlit as st

from utils.batch_api_client import (
    batch_predict_csv
)


def render_batch_intelligence():

    st.header(
        "Batch Intelligence Center"
    )

    st.markdown(
        """
        Upload a shipment CSV,
        generate predictions,
        and explore risk insights.
        """
    )

    uploaded_file = (
        st.file_uploader(

            "Upload Shipment CSV",

            type=["csv"]
        )
    )

    if uploaded_file:

        if st.button(

            "Run Batch Prediction"
        ):

            try:

                with st.spinner(

                    "Processing shipments..."
                ):

                    csv_bytes = (
                        batch_predict_csv(
                            uploaded_file
                        )
                    )

                result_df = (
                    pd.read_csv(
                        io.BytesIO(
                            csv_bytes
                        )
                    )
                )

                st.session_state[
                    "batch_df"
                ] = result_df

                st.success(
                    "Batch Prediction Complete"
                )

                # ==========================
                # KPI CARDS
                # ==========================

                total_shipments = len(
                    result_df
                )

                critical_count = (

                    result_df[
                        "predicted_risk"
                    ]
                    ==
                    "Critical"

                ).sum()

                medium_count = (

                    result_df[
                        "predicted_risk"
                    ]
                    ==
                    "Medium"

                ).sum()

                low_count = (

                    result_df[
                        "predicted_risk"
                    ]
                    ==
                    "Low"

                ).sum()

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                with col1:

                    st.metric(
                        "Total Shipments",
                        total_shipments
                    )

                with col2:

                    st.metric(
                        "Critical",
                        critical_count
                    )

                with col3:

                    st.metric(
                        "Medium",
                        medium_count
                    )

                with col4:

                    st.metric(
                        "Low",
                        low_count
                    )

                st.divider()

                # ==========================
                # RISK DISTRIBUTION
                # ==========================

                st.subheader(
                    "Risk Distribution"
                )

                risk_counts = (

                    result_df[
                        "predicted_risk"
                    ]

                    .value_counts()

                    .reset_index()
                )

                risk_counts.columns = [

                    "Risk",

                    "Count"
                ]

                fig = px.bar(

                    risk_counts,

                    x="Risk",

                    y="Count",

                    title=(
                        "Predicted "
                        "Risk Distribution"
                    )
                )

                st.plotly_chart(

                    fig,

                    use_container_width=True
                )

                st.divider()

                # ==========================
                # CONFIDENCE HISTOGRAM
                # ==========================

                st.subheader(
                    "Model Confidence Distribution"
                )

                fig = px.histogram(

                    result_df,

                    x="model_confidence",

                    nbins=20,

                    title=(
                        "Confidence "
                        "Distribution"
                    )
                )

                st.plotly_chart(

                    fig,

                    use_container_width=True
                )

                st.divider()

                # ==========================
                # RISK SCORE HISTOGRAM
                # ==========================

                st.subheader(
                    "Risk Score Distribution"
                )

                fig = px.histogram(

                    result_df,

                    x="risk_score",

                    nbins=20,

                    title=(
                        "Risk Score "
                        "Distribution"
                    )
                )

                st.plotly_chart(

                    fig,

                    use_container_width=True
                )

                st.divider()

                # ==========================
                # TOP HIGH-RISK CONTAINERS
                # ==========================

                st.subheader(
                    "Top High-Risk Containers"
                )

                top_risk_df = (

                    result_df

                    .sort_values(

                        "risk_score",

                        ascending=False
                    )

                    .head(100)
                )

                st.dataframe(

                    top_risk_df,

                    use_container_width=True
                )

                st.divider()

                # ==========================
                # DOWNLOAD RESULTS
                # ==========================

                st.download_button(

                    label=
                    "Download Predictions CSV",

                    data=csv_bytes,

                    file_name=
                    "predictions.csv",

                    mime=
                    "text/csv"
                )

            except Exception as e:

                st.error(

                    f"Batch prediction failed: "
                    f"{str(e)}"
                )