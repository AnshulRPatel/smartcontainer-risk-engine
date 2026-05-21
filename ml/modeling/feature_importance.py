import pandas as pd

import matplotlib.pyplot as plt

from ml.modeling.inference import (
    load_model
)

from ml.modeling.preprocess import (
    FEATURE_COLUMNS
)


def analyze_feature_importance():

    print(
        "Loading trained model..."
    )

    model = load_model()

    print(
        "Extracting feature importances..."
    )

    importances = (
        model.get_feature_importance()
    )

    importance_df = pd.DataFrame({

        "Feature": FEATURE_COLUMNS,

        "Importance": importances
    })

    importance_df = (

        importance_df

        .sort_values(
            "Importance",
            ascending=False
        )

        .reset_index(drop=True)
    )

    print(
        "\n========== FEATURE IMPORTANCE ==========\n"
    )

    print(importance_df)

    # Save CSV

    importance_df.to_csv(

        "outputs/metrics/feature_importance.csv",

        index=False
    )

    # Plot Top 15

    top_features = (
        importance_df.head(15)
    )

    plt.figure(figsize=(12, 8))

    plt.barh(

        top_features["Feature"][::-1],

        top_features["Importance"][::-1]
    )

    plt.xlabel("Importance Score")

    plt.ylabel("Feature")

    plt.title(
        "Top 15 Feature Importances"
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/feature_importance.png"
    )

    plt.show()

    print(
        "\nFeature importance analysis complete."
    )


if __name__ == "__main__":

    analyze_feature_importance()