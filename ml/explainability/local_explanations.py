import pandas as pd

import shap

import matplotlib.pyplot as plt

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


def generate_local_explanations():

    print(
        "Loading anomaly shipment dataset..."
    )

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

    print(
        "Loading trained model..."
    )

    model = load_model()

    print(
        "Creating SHAP explainer..."
    )

    explainer = shap.TreeExplainer(
        model
    )

    print(
        "Calculating SHAP values..."
    )

    shap_values = explainer.shap_values(
        X_test
    )

    # =========================
    # CRITICAL CLASS SHAP
    # =========================

    critical_class_shap = (
        shap_values[:, :, 0]
    )

    # =========================
    # SELECT MOST ANOMALOUS SHIPMENT
    # =========================

    critical_index = 0

    shipment_data = (
        X_test.iloc[critical_index]
    )

    shipment_shap = (
        critical_class_shap[critical_index]
    )

    print(
        "\nGenerating waterfall plot..."
    )

    shap.plots.waterfall(

        shap.Explanation(

            values=shipment_shap,

            base_values=explainer.expected_value[0],

            data=shipment_data,

            feature_names=X_test.columns
        ),

        show=False
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/shap/local_waterfall.png"
    )

    plt.close()

    print(
        "Generating force plot..."
    )

    force_plot = shap.force_plot(

        explainer.expected_value[0],

        shipment_shap,

        shipment_data,

        matplotlib=True,

        show=False
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/shap/local_force_plot.png"
    )

    plt.close()

    print(
        "\nGenerating local explanation CSV..."
    )

    local_df = pd.DataFrame({

        "Feature": X_test.columns,

        "Feature_Value": shipment_data.values,

        "SHAP_Contribution": shipment_shap
    })

    local_df = (

        local_df

        .sort_values(

            "SHAP_Contribution",

            ascending=False
        )
    )

    local_df.to_csv(

        "outputs/metrics/local_shap_explanation.csv",

        index=False
    )

    print(
        "\nLocal explainability complete."
    )


if __name__ == "__main__":

    generate_local_explanations()