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


def run_shap_analysis():

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

    print(
        "\nEncoded Label Mapping:"
    )

    print(
        dict(
            enumerate(
                label_encoder.classes_
            )
        )
    )

    # =========================
    # MULTICLASS SHAP FIX
    # =========================

    # SHAP returns:
    # (samples, features, classes)

    critical_class_shap = (
        shap_values[:, :, 0]
    )

    print(
        "\nGenerating SHAP summary plot..."
    )

    shap.summary_plot(

        critical_class_shap,

        X_test,

        show=False
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/shap/shap_summary.png"
    )

    plt.close()

    print(
        "Generating SHAP bar plot..."
    )

    shap.summary_plot(

        critical_class_shap,

        X_test,

        plot_type="bar",

        show=False
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/shap/shap_bar.png"
    )

    plt.close()

    print(
        "Generating dependence plot..."
    )

    shap.dependence_plot(

        "Declared_Value",

        critical_class_shap,

        X_test,

        show=False
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/shap/declared_value_dependence.png"
    )

    plt.close()

    print(
        "\nSHAP explainability complete."
    )


if __name__ == "__main__":

    run_shap_analysis()