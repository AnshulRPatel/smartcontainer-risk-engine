import streamlit as st

import plotly.express as px


def render_anomaly_intelligence(df):

    st.header(
        "Anomaly Intelligence"
    )

    # =========================
    # VALUE VS WEIGHT
    # =========================

    fig1 = px.scatter(

        df,

        x="Declared_Weight",

        y="Declared_Value",

        color="Risk_Label",

        size=(
            abs(
                df[
                    "Weight_Difference_Percent"
                ]
            )
        ),

        hover_data=[
            "Container_ID"
        ],

        title=(
            "Value vs Weight Anomalies"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =========================
    # DWELL-TIME RISK
    # =========================

    fig2 = px.box(

        df,

        x="Risk_Label",

        y="Dwell_Time_Hours",

        color="Risk_Label",

        title=(
            "Dwell-Time Distribution"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =========================
    # ANOMALY SCORE DENSITY
    # =========================

    fig3 = px.histogram(

        df,

        x="Anomaly_Score",

        color="Risk_Label",

        nbins=80,

        marginal="box",

        title=(
            "Anomaly Score Density"
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =========================
    # TOP ANOMALOUS SHIPMENTS
    # =========================

    st.subheader(
        "Most Anomalous Shipments"
    )

    top_anomalies = (

        df

        .sort_values(
            "Anomaly_Score"
        )

        .head(20)
    )

    display_cols = [

        "Container_ID",

        "Risk_Label",

        "Anomaly_Score",

        "Declared_Value",

        "Weight_Difference_Percent",

        "Dwell_Time_Hours"
    ]

    st.dataframe(
        top_anomalies[
            display_cols
        ]
    )