import streamlit as st


def render_kpi_cards(metrics):

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(

        "Total Shipments",

        metrics[
            "total_shipments"
        ]
    )

    col2.metric(

        "Critical Risk",

        metrics[
            "critical_count"
        ]
    )

    col3.metric(

        "Medium Risk",

        metrics[
            "medium_count"
        ]
    )

    col4.metric(

        "Avg Anomaly Score",

        round(
            metrics[
                "avg_anomaly_score"
            ],
            3
        )
    )