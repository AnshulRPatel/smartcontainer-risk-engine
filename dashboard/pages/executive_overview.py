import streamlit as st

from components.kpi_cards import (
    render_kpi_cards
)

from components.risk_charts import (

    render_risk_distribution,

    render_anomaly_distribution
)


def render_executive_overview(

    df,

    metrics
):

    st.header(
        "Executive Risk Overview"
    )

    render_kpi_cards(metrics)

    st.divider()

    render_risk_distribution(df)

    st.divider()

    render_anomaly_distribution(df)