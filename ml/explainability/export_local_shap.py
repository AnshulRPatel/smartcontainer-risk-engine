# test comment
import pandas as pd

import shap

from ml.modeling.inference import (
    load_model
)

from ml.modeling.preprocess import (
    prepare_training_data
)

from ml.modeling.config import (

    TARGET_COLUMN,

    TEST_SIZE,

    RANDOM_STATE
)


def export_local_shap():

    df = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

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

    model = load_model()

    explainer = shap.TreeExplainer(
        model
    )

    shap_values = explainer.shap_values(
        X_test
    )

    critical_class_shap = (
        shap_values[:, :, 0]
    )

    shap_df = pd.DataFrame(

        critical_class_shap,

        columns=X_test.columns
    )

    shap_df["Container_ID"] = (
        df.iloc[
            X_test.index
        ]["Container_ID"]
        .values
    )

    shap_df.to_csv(

        "outputs/metrics/local_shap_values.csv",

        index=False
    )

    print(
        "Local SHAP export complete."
    )


if __name__ == "__main__":

    export_local_shap()