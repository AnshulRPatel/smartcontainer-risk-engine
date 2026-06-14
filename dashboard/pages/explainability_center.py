import os

import pandas as pd

import streamlit as st


def render_explainability_center():

    st.header(
        "Explainability Center"
    )

    # ==========================================
    # FILE PATHS
    # ==========================================

    explanations_path = (
        "outputs/reports/"
        "prediction_explanations_reference.csv"
    )

    shap_values_path = (
        "outputs/metrics/"
        "local_shap_values.csv"
    )

    shap_summary_path = (
        "outputs/plots/shap/"
        "shap_summary.png"
    )

    shap_bar_path = (
        "outputs/plots/shap/"
        "shap_bar.png"
    )

    # ==========================================
    # VALIDATE REQUIRED FILES
    # ==========================================

    required_files = [
        explanations_path,
        shap_values_path,
        shap_summary_path,
        shap_bar_path
    ]

    missing_files = [

        file_path

        for file_path in required_files

        if not os.path.exists(file_path)
    ]

    # ==========================================
    # HANDLE MISSING FILES
    # ==========================================

    if missing_files:

        st.warning(
            """
            Explainability artifacts are not available yet.

            Please run:
            - Live Prediction
            OR
            - Batch Intelligence

            to generate SHAP explanations and reports.
            """
        )

        st.subheader(
            "Missing Files"
        )

        for file_path in missing_files:

            st.code(file_path)

        return

    # ==========================================
    # LOAD DATA
    # ==========================================

    explanations = pd.read_csv(
        explanations_path
    )

    shap_values = pd.read_csv(
        shap_values_path
    )

    # ==========================================
    # GLOBAL EXPLAINABILITY
    # ==========================================

    st.subheader(
        "Global SHAP Summary"
    )

    st.image(
        shap_summary_path
    )

    st.subheader(
        "Feature Importance"
    )

    st.image(
        shap_bar_path
    )

    st.divider()

    # ==========================================
    # LOCAL EXPLAINABILITY
    # ==========================================

    st.subheader(
        "Shipment-Level Explanation"
    )

    container_id = st.text_input(
        "Enter Container ID for SHAP analysis"
    )

    if container_id:

        local_exp = explanations[

            explanations[
                "Container_ID"
            ]
            .astype(str)

            == str(container_id)
        ]

        local_shap = shap_values[

            shap_values[
                "Container_ID"
            ]
            .astype(str)

            == str(container_id)
        ]

        if len(local_exp) > 0 and len(local_shap) > 0:

            st.markdown(

                f"""
                ### Operational Explanation

                **Risk Label:**  
                {local_exp.iloc[0]['Risk_Label']}

                **Explanation:**  
                {local_exp.iloc[0]['Explanation_Summary']}
                """
            )

            st.subheader(
                "Top SHAP Contributors"
            )

            shap_display = (

                local_shap

                .drop(
                    columns=["Container_ID"]
                )

                .iloc[0]

                .reset_index()
            )

            shap_display.columns = [
                "Feature",
                "Contribution"
            ]

            shap_display = (

                shap_display

                .sort_values(
                    "Contribution",
                    ascending=False
                )

                .head(10)
            )

            st.dataframe(
                shap_display
            )

        else:

            st.warning(
                "Container ID does not exist or "
                "local SHAP explanation "
                "is unavailable for this shipment."
            )

