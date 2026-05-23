import streamlit as st


def render_sidebar_filters(df):

    st.sidebar.header(
        "Dashboard Filters"
    )

    risk_levels = st.sidebar.multiselect(

        "Risk Level",

        options=sorted(
            df["Risk_Label"]
            .unique()
        ),

        default=sorted(
            df["Risk_Label"]
            .unique()
        )
    )

    trade_regimes = st.sidebar.multiselect(

        "Trade Regime",

        options=sorted(
            df["Trade_Regime"]
            .unique()
        ),

        default=sorted(
            df["Trade_Regime"]
            .unique()
        )
    )

    filtered_df = df[

        (
            df["Risk_Label"]
            .isin(risk_levels)
        )

        &

        (
            df["Trade_Regime"]
            .isin(trade_regimes)
        )
    ]

    return filtered_df