from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline


def train_isolation_forest(df, feature_cols):

    pipeline = Pipeline([

        (
            "imputer",
            SimpleImputer(strategy="median")
        ),

        (
            "scaler",
            RobustScaler()
        ),

        (
            "model",
            IsolationForest(
                n_estimators=300,
                contamination=0.02,
                random_state=42,
                n_jobs=-1
            )
        )
    ])

    pipeline.fit(df[feature_cols])

    df["Anomaly_Score"] = (
        pipeline.named_steps["model"]
        .decision_function(
            pipeline[:-1].transform(df[feature_cols])
        )
    )

    df["Anomaly_Flag"] = (
        pipeline.named_steps["model"]
        .predict(
            pipeline[:-1].transform(df[feature_cols])
        )
    )

    # Convert:
    # -1 → anomaly
    #  1 → normal

    df["Anomaly_Flag"] = (
        df["Anomaly_Flag"] == -1
    ).astype(int)

    return df, pipeline