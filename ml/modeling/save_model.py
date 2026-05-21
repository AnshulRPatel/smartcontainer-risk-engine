from ml.modeling.config import (
    MODEL_PATH
)


def save_trained_model(model):

    print("\nSaving model...\n")

    model.save_model(MODEL_PATH)

    print(
        f"Model saved to: {MODEL_PATH}"
    )