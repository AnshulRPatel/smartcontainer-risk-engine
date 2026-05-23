import pandas as pd

import streamlit as st


def render_explainability_center():

    st.header(
        "Explainability Center"
    )

    explanations = pd.read_csv(
        "outputs/reports/prediction_explanations.csv"
    )

    shap_values = pd.read_csv(
        "outputs/metrics/local_shap_values.csv"
    )

    # =========================
    # GLOBAL EXPLAINABILITY
    # =========================

    st.subheader(
        "Global SHAP Summary"
    )

    st.image(
        "outputs/plots/shap/shap_summary.png"
    )

    st.subheader(
        "Feature Importance"
    )

    st.image(
        "outputs/plots/shap/shap_bar.png"
    )

    st.divider()

    # =========================
    # LOCAL EXPLAINABILITY
    # =========================

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