import pandas as pd

from sklearn.metrics import (

    classification_report,

    confusion_matrix,

    accuracy_score,

    f1_score
)


def evaluate_model(
    y_test,
    y_pred
):

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    macro_f1 = f1_score(
        y_test,
        y_pred,
        average="macro"
    )

    report = classification_report(
        y_test,
        y_pred
    )

    matrix = confusion_matrix(
        y_test,
        y_pred
    )

    return {

        "accuracy": accuracy,

        "macro_f1": macro_f1,

        "classification_report": report,

        "confusion_matrix": matrix
    }


def save_evaluation_outputs(results):

    with open(
        "outputs/reports/classification_report.txt",
        "w"
    ) as f:

        f.write(
            results["classification_report"]
        )

    pd.DataFrame(
        results["confusion_matrix"]
    ).to_csv(
        "outputs/metrics/confusion_matrix.csv",
        index=False
    )