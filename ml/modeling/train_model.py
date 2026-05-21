from datetime import datetime

import pandas as pd

import mlflow
import mlflow.catboost

from catboost import (
    CatBoostClassifier
)

from ml.modeling.preprocess import (

    prepare_training_data,

    CATEGORICAL_FEATURES
)

from ml.modeling.evaluate_model import (

    evaluate_model,

    save_evaluation_outputs
)

from ml.modeling.save_model import (
    save_trained_model
)

from ml.modeling.config import (

    TARGET_COLUMN,

    RANDOM_STATE,

    TEST_SIZE,

    EXPERIMENT_NAME,

    EXPERIMENT_PHASE,

    MODEL_NAME,

    CATBOOST_PARAMS
)


mlflow.set_tracking_uri(
    "file:./mlruns"
)


def train_catboost_model():

    print("Loading anomaly shipment dataset...")

    df = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

    print(f"Dataset Shape: {df.shape}")

    (
        X_train,
        X_test,
        y_train,
        y_test,
        label_encoder,
        selected_features
    ) = prepare_training_data(

        df=df,

        target_col=TARGET_COLUMN,

        test_size=TEST_SIZE,

        random_state=RANDOM_STATE
    )

    categorical_indices = [

        X_train.columns.get_loc(col)

        for col in CATEGORICAL_FEATURES

        if col in X_train.columns
    ]

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    run_name = (

        f"{MODEL_NAME}_"

        f"{EXPERIMENT_PHASE}_"

        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    with mlflow.start_run(
        run_name=run_name
    ):

        mlflow.set_tags({

            "model_type": MODEL_NAME,

            "experiment_phase": EXPERIMENT_PHASE,

            "feature_count": len(
                selected_features
            ),

            "pipeline_stage": "supervised_modeling"
        })

        model = CatBoostClassifier(
            **CATBOOST_PARAMS
        )

        print("\nTraining CatBoost model...\n")

        model.fit(

            X_train,

            y_train,

            cat_features=categorical_indices,

            eval_set=(X_test, y_test),

            verbose=100
        )

        print("\nGenerating predictions...\n")

        y_pred = model.predict(X_test)

        results = evaluate_model(
            y_test,
            y_pred
        )

        print("\n========== MODEL PERFORMANCE ==========\n")

        print(
            f"Accuracy: "
            f"{results['accuracy']:.4f}"
        )

        print(
            f"Macro F1 Score: "
            f"{results['macro_f1']:.4f}"
        )

        print("\nClassification Report:\n")

        print(
            results["classification_report"]
        )

        print("\nConfusion Matrix:\n")

        print(
            results["confusion_matrix"]
        )

        save_trained_model(model)

        save_evaluation_outputs(
            results
        )

        mlflow.log_params(
            CATBOOST_PARAMS
        )

        mlflow.log_metric(
            "accuracy",
            results["accuracy"]
        )

        mlflow.log_metric(
            "macro_f1",
            results["macro_f1"]
        )

        mlflow.log_param(
            "feature_count",
            len(selected_features)
        )

        mlflow.catboost.log_model(
            model,
            name="catboost_model"
        )

        print("\nTraining complete.")


if __name__ == "__main__":

    train_catboost_model()