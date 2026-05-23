import streamlit as st

from components.queue_table import (
    render_critical_queue
)


def render_operational_queue(df):

    st.header(
        "Operational Risk Queue"
    )

    st.markdown(
        """
        Monitor and investigate
        high-risk shipments flagged
        by the AI risk engine.
        """
    )

    render_critical_queue(df)