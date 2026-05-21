from catboost import (
    CatBoostClassifier
)

from ml.modeling.config import (
    MODEL_PATH
)


def load_model():

    model = CatBoostClassifier()

    model.load_model(MODEL_PATH)

    return model


def predict_risk(model, X):

    predictions = model.predict(X)

    probabilities = (
        model.predict_proba(X)
    )

    return (
        predictions,
        probabilities
    )