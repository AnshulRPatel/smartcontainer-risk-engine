import plotly.express as px

import streamlit as st


def render_risk_distribution(df):

    st.subheader(
        "Risk Distribution"
    )

    risk_counts = (

        df["Risk_Label"]

        .value_counts()

        .reset_index()
    )

    risk_counts.columns = [
        "Risk_Label",
        "Count"
    ]

    fig = px.bar(

        risk_counts,

        x="Risk_Label",

        y="Count",

        color="Risk_Label",

        title="Shipment Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_anomaly_distribution(df):

    st.subheader(
        "Anomaly Score Distribution"
    )

    fig = px.histogram(

        df,

        x="Anomaly_Score",

        color="Risk_Label",

        nbins=50,

        title="Anomaly Score Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )