import streamlit as st

import plotly.express as px


def render_importer_exporter_profiles(df):

    st.header(
        "Behavioral Intelligence"
    )

    # =========================
    # IMPORTER RISK ANALYSIS
    # =========================

    importer_stats = (

        df.groupby(
            "Importer_ID"
        )

        .agg({

            "Total_Risk_Score": "mean",

            "Anomaly_Score": "mean",

            "Container_ID": "count"
        })

        .reset_index()
    )

    importer_stats.columns = [

        "Importer_ID",

        "Avg_Risk_Score",

        "Avg_Anomaly_Score",

        "Shipment_Count"
    ]

    # =========================
# POSITIVE SIZE SCALING
# =========================

    importer_stats[
        "Bubble_Size"
    ] = (

        importer_stats[
            "Avg_Anomaly_Score"
        ]
        .abs()
    )

    fig = px.scatter(

        importer_stats,

        x="Shipment_Count",

        y="Avg_Risk_Score",

        size="Bubble_Size",

        hover_data=[
            "Importer_ID"
        ],

        title=(
            "Importer Behavioral Risk"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # TOP RISKY IMPORTERS
    # =========================

    st.subheader(
        "Top Risky Importers"
    )

    risky_importers = (

        importer_stats

        .sort_values(
            "Avg_Risk_Score",
            ascending=False
        )

        .head(20)
    )

    st.dataframe(
        risky_importers
    )