import pandas as pd
import numpy as np
from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    LabelEncoder
)

from ml.modeling.config import (

    ENABLE_ANOMALY_FEATURES,

    ENABLE_BEHAVIORAL_FEATURES,

    ENABLE_TEMPORAL_FEATURES,

    ENABLE_LOG_FEATURES,

    ENABLE_CORRELATION_PRUNING,

    CORRELATION_THRESHOLD
)


BASE_FEATURES = [

    "Declared_Value",

    "Declared_Weight",

    

    "Dwell_Time_Hours",

    "Weight_Difference",

    "Weight_Difference_Percent",

    "Value_Per_Weight",

    "was_zero_declared_weight",

    

    "Trade_Regime",

    

    "Destination_Country",

    "Destination_Port",

    "Shipping_Line",

    "HS_Chapter"
]


ANOMALY_FEATURES = [

    

    "Anomaly_Score",

    "High_Weight_Anomaly",

    "Excessive_Dwell_Flag"
]


BEHAVIORAL_FEATURES = [

    

    "Exporter_Shipment_Count",

    "Shipping_Line_Frequency"
]


TEMPORAL_FEATURES = [

    "Declaration_Weekday",

    "Declaration_Hour",

    

    "Is_Night_Declaration"
]


LOG_FEATURES = [

    "Log_Declared_Value"

    
]


CATEGORICAL_FEATURES = [

    "Trade_Regime",

    "Origin_Country",

    "Destination_Country",

    "Destination_Port",

    "Shipping_Line",

    "HS_Chapter"
]


def build_feature_list():

    features = BASE_FEATURES.copy()

    if ENABLE_ANOMALY_FEATURES:

        features.extend(
            ANOMALY_FEATURES
        )

    if ENABLE_BEHAVIORAL_FEATURES:

        features.extend(
            BEHAVIORAL_FEATURES
        )

    if ENABLE_TEMPORAL_FEATURES:

        features.extend(
            TEMPORAL_FEATURES
        )

    if ENABLE_LOG_FEATURES:

        features.extend(
            LOG_FEATURES
        )

    return features


FEATURE_COLUMNS = build_feature_list()


def remove_correlated_features(df):

    numeric_df = (
        df[FEATURE_COLUMNS]
        .select_dtypes(include=["number"])
    )

    corr_matrix = numeric_df.corr().abs()

    upper_triangle = corr_matrix.where(

        pd.np.triu(
            pd.np.ones(
                corr_matrix.shape
            ),
            k=1
        ).astype(bool)
    )

    to_drop = [

        column

        for column in upper_triangle.columns

        if any(
            upper_triangle[column]
            > CORRELATION_THRESHOLD
        )
    ]

    filtered_features = [

        col

        for col in FEATURE_COLUMNS

        if col not in to_drop
    ]

    return filtered_features


def prepare_training_data(
    df,
    target_col,
    test_size,
    random_state
):

    features = FEATURE_COLUMNS

    if ENABLE_CORRELATION_PRUNING:

        features = (
            remove_correlated_features(df)
        )

    X = df[features]

    y = df[target_col]

    label_encoder = LabelEncoder()

    y_encoded = (
        label_encoder.fit_transform(y)
    )

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y_encoded,

            test_size=test_size,

            stratify=y_encoded,

            random_state=random_state
        )
    )

    return (

        X_train,

        X_test,

        y_train,

        y_test,

        label_encoder,

        features
    )

def prepare_inference_data(df):

    inference_df = df.copy()

    # =========================
    # DATETIME PROCESSING
    # =========================

    inference_df[
        "Declaration_Date"
    ] = pd.to_datetime(

        inference_df[
            "Declaration_Date"
        ],

        errors="coerce"
    )

    inference_df[
        "Declaration_Hour"
    ] = (

        pd.to_datetime(

            inference_df[
                "Declaration_Time"
            ],

            format="%H:%M:%S",

            errors="coerce"
        )

        .dt.hour
    )

    inference_df[
        "Declaration_Weekday"
    ] = (

        inference_df[
            "Declaration_Date"
        ]
        .dt.weekday
    )

    inference_df[
        "Is_Night_Declaration"
    ] = (

        inference_df[
            "Declaration_Hour"
        ]
        .between(0, 5)

    ).astype(int)

    # =========================
    # WEIGHT FEATURES
    # =========================

    inference_df[
        "Weight_Difference"
    ] = (

        inference_df[
            "Measured_Weight"
        ]

        -

        inference_df[
            "Declared_Weight"
        ]
    )

    inference_df[
        "Weight_Difference_Percent"
    ] = (

        inference_df[
            "Weight_Difference"
        ]

        /

        (
            inference_df[
                "Declared_Weight"
            ] + 1
        )
    ) * 100

    # =========================
    # VALUE FEATURES
    # =========================

    inference_df[
        "Value_Per_Weight"
    ] = (

        inference_df[
            "Declared_Value"
        ]

        /

        (
            inference_df[
                "Declared_Weight"
            ] + 1
        )
    )

    inference_df[
        "Log_Declared_Value"
    ] = np.log(

        inference_df[
            "Declared_Value"
        ] + 1
    )

    inference_df[
        "was_zero_declared_weight"
    ] = (

        inference_df[
            "Declared_Weight"
        ] == 0
    ).astype(int)

    # =========================
    # HS CHAPTER
    # =========================

    inference_df[
        "HS_Chapter"
    ] = (

        inference_df[
            "HS_Code"
        ]
        .astype(str)
        .str[:2]
    )

    # =========================
    # PLACEHOLDER FEATURES
    # =========================

    inference_df[
        "Anomaly_Score"
    ] = 0.0

    inference_df[
        "High_Weight_Anomaly"
    ] = (

        inference_df[
            "Weight_Difference_Percent"
        ].abs() > 30

    ).astype(int)

    inference_df[
        "Excessive_Dwell_Flag"
    ] = (

        inference_df[
            "Dwell_Time_Hours"
        ] > 72

    ).astype(int)

    inference_df[
        "Exporter_Shipment_Count"
    ] = 1

    inference_df[
        "Shipping_Line_Frequency"
    ] = 1

    # =========================
    # BUILD FINAL FEATURE SET
    # =========================

    features = FEATURE_COLUMNS

    if ENABLE_CORRELATION_PRUNING:

        features = [

            col

            for col in features

            if col in inference_df.columns
        ]

    final_df = inference_df[
        features
    ].copy()

    # =========================
    # CATEGORICAL TYPES
    # =========================

    for col in CATEGORICAL_FEATURES:

        if col in final_df.columns:

            final_df[col] = (

                final_df[col]
                .astype(str)
            )

    return final_df