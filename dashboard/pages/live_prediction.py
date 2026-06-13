import streamlit as st

from dashboard.utils.api_client import (
    predict_shipment,

    explain_shipment
)


def render_live_prediction():

    st.header(
        "Live Shipment Prediction"
    )

    st.markdown(
        """
        Submit a shipment to the
        production FastAPI service.
        """
    )

    with st.form(
        "prediction_form"
    ):

        container_id = st.text_input(
            "Container ID"
        )

        declaration_date = (
            st.text_input(
                "Declaration Date",
                "2020-01-02"
            )
        )

        declaration_time = (
            st.text_input(
                "Declaration Time",
                "20:56:03"
            )
        )

        trade_regime = (
            st.selectbox(
                "Trade Regime",
                [
                    "Import",
                    "Export"
                ]
            )
        )

        origin_country = (
            st.text_input(
                "Origin Country",
                "CN"
            )
        )

        destination_port = (
            st.text_input(
                "Destination Port",
                "PORT_40"
            )
        )

        destination_country = (
            st.text_input(
                "Destination Country",
                "RS"
            )
        )

        hs_code = st.text_input(
            "HS Code",
            "610910"
        )

        importer_id = (
            st.text_input(
                "Importer ID"
            )
        )

        exporter_id = (
            st.text_input(
                "Exporter ID"
            )
        )

        declared_value = (
            st.number_input(
                "Declared Value",
                value=624.0
            )
        )

        declared_weight = (
            st.number_input(
                "Declared Weight",
                value=40.0
            )
        )

        measured_weight = (
            st.number_input(
                "Measured Weight",
                value=48.298
            )
        )

        shipping_line = (
            st.text_input(
                "Shipping Line",
                "LINE_MODE_40"
            )
        )

        dwell_time = (
            st.number_input(
                "Dwell Time Hours",
                value=93.4
            )
        )

        submit = (
            st.form_submit_button(
                "Predict"
            )
        )

    if submit:

        payload = {

            "Container_ID":
            container_id,

            "Declaration_Date":
            declaration_date,

            "Declaration_Time":
            declaration_time,

            "Trade_Regime":
            trade_regime,

            "Origin_Country":
            origin_country,

            "Destination_Port":
            destination_port,

            "Destination_Country":
            destination_country,

            "HS_Code":
            hs_code,

            "Importer_ID":
            importer_id,

            "Exporter_ID":
            exporter_id,

            "Declared_Value":
            declared_value,

            "Declared_Weight":
            declared_weight,

            "Measured_Weight":
            measured_weight,

            "Shipping_Line":
            shipping_line,

            "Dwell_Time_Hours":
            dwell_time
        }

        try:

            result = (
                predict_shipment(
                    payload
                )
            )

            explanation_result = (
                explain_shipment(
                    payload
                )
            )

            st.success(
                "Prediction Completed"
            )

            if (
                result[
                    "predicted_risk"
                ]
                ==
                "Critical"
            ):

                st.error(
                    "🔴 Critical Risk Shipment"
                )

            elif (
                result[
                    "predicted_risk"
                ]
                ==
                "Medium"
            ):

                st.warning(
                    "🟠 Medium Risk Shipment"
                )

            else:

                st.success(
                    "🟢 Low Risk Shipment"
                )

            # ==========================
            # KPI ROW
            # ==========================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Predicted Risk",

                    result[
                        "predicted_risk"
                    ]
                )

            with col2:

                st.metric(

                    "Risk Label",

                    result[
                        "risk_label"
                    ]
                )

            with col3:

                st.metric(

                    "Model Confidence",

                    f"{result['model_confidence']:.1%}"
                )

            # ==========================
            # SCORES
            # ==========================

            st.subheader(
                "Risk Scores"
            )

            score_col1, score_col2 = (
                st.columns(2)
            )

            with score_col1:

                st.metric(

                    "Risk Score",

                    result[
                        "risk_score"
                    ]
                )

            with score_col2:

                st.metric(

                    "Anomaly Score",

                    round(

                        result[
                            "anomaly_score"
                        ],

                        3
                    )
                )

            # ==========================
            # EXPLANATION
            # ==========================

            st.subheader(
                "Explanation"
            )

            st.info(

                result[
                    "explanation"
                ]
            )

            # ==========================
            # TOP RISK FACTORS
            # ==========================

            st.subheader(
                "Top Risk Factors"
            )

            risk_factors = (

                explanation_result.get(

                    "top_risk_factors",

                    []
                )
            )

            if risk_factors:

                for factor in risk_factors:

                    col1, col2 = st.columns(
                        [3, 1]
                    )

                    with col1:

                        st.write(
                            factor[
                                "factor"
                            ]
                        )

                    with col2:

                        st.metric(

                            "Value",

                            factor[
                                "value"
                            ]
                        )

            else:

                st.success(

                    "No significant risk "
                    "factors detected."
                )

            # ==========================
            # RAW API RESPONSE
            # ==========================

            with st.expander(

                "Raw API Response"
            ):

                st.json(
                    explanation_result
                )

        except Exception as e:

            st.error(
                str(e)
            )