import pandas as pd

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