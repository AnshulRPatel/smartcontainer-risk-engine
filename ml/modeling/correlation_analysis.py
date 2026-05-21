import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

from ml.modeling.preprocess import (
    FEATURE_COLUMNS
)


def analyze_feature_correlations():

    print(
        "Loading anomaly shipment dataset..."
    )

    df = pd.read_csv(
        "data/processed/anomaly_shipments.csv"
    )

    numeric_features = (

        df[FEATURE_COLUMNS]

        .select_dtypes(
            include=["number"]
        )
    )

    correlation_matrix = (
        numeric_features.corr()
    )

    print(
        "\n========== CORRELATION MATRIX ==========\n"
    )

    print(correlation_matrix)

    correlation_matrix.to_csv(

        "outputs/metrics/correlation_matrix.csv"
    )

    plt.figure(figsize=(16, 12))

    sns.heatmap(

        correlation_matrix,

        cmap="coolwarm",

        center=0
    )

    plt.title(
        "Feature Correlation Heatmap"
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/plots/correlation_heatmap.png"
    )

    plt.show()

    print(
        "\nCorrelation analysis complete."
    )


if __name__ == "__main__":

    analyze_feature_correlations()