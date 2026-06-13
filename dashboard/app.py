import streamlit as st

from dashboard.utils.data_loader import (
    load_dashboard_data
)

from dashboard.utils.metrics import (
    compute_dashboard_metrics
)

from dashboard.components.sidebar_filters import (
    render_sidebar_filters
)

from dashboard.pages.executive_overview import (
    render_executive_overview
)

from dashboard.pages.operational_queue import (
    render_operational_queue
)

from dashboard.pages.anomaly_intelligence import (
    render_anomaly_intelligence
)

from dashboard.pages.explainability_center import (
    render_explainability_center
)
from dashboard.pages.importer_exporter_profiles import (
    render_importer_exporter_profiles
)

from dashboard.pages.live_prediction import (
    render_live_prediction
)

from dashboard.pages.batch_intelligence import (
    render_batch_intelligence
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title=(
        "Customs Risk Intelligence"
    ),

    layout="wide"
)


# =========================
# LOAD DATA
# =========================

df = load_dashboard_data()

filtered_df = (
    render_sidebar_filters(df)
)

metrics = (
    compute_dashboard_metrics(
        filtered_df
    )
)


# =========================
# SIDEBAR NAVIGATION
# =========================

st.sidebar.title(
    "Navigation"
)

page = st.sidebar.radio(

    "Select Dashboard Page",

    [

        "Executive Overview",

        "Operational Queue",

        "Anomaly Intelligence",

        "Behavioral Intelligence",

        "Explainability Center",

        "Live Prediction",

        "Batch Intelligence Center"
    ]
)


# =========================
# MAIN TITLE
# =========================

st.title(
    "🚢 SmartContainer Risk Engine"
)

st.markdown(
    """
    AI-powered customs shipment
    risk monitoring and anomaly
    detection platform.
    """
)


# =========================
# PAGE ROUTING
# =========================

if page == "Executive Overview":

    render_executive_overview(

        filtered_df,

        metrics
    )

elif page == "Operational Queue":

    render_operational_queue(
        filtered_df
    )

elif page == "Anomaly Intelligence":

    render_anomaly_intelligence(
        filtered_df
    )

elif page == "Explainability Center":

    render_explainability_center()

elif page == "Behavioral Intelligence":

    render_importer_exporter_profiles(
        filtered_df
    )

elif page == "Live Prediction":

    render_live_prediction()

elif page == (
    "Batch Intelligence Center"
):

    render_batch_intelligence()        