import pandas as pd

from ml.modeling.inference import (
    load_model
)

from ml.modeling.preprocess import (
    prepare_inference_data
)

from app.services.context_service import (
    context_service
)


# ============================================
# LOAD DATASET
# ============================================

df = pd.read_csv(
    "data/processed/anomaly_shipments.csv"
)

# ============================================
# SELECT CONTAINER
# ============================================

row = df[
    df["Container_ID"] == 88268883
].copy()

print("\n========== RAW ROW ==========\n")

print(row.T)

# ============================================
# LOAD MODEL
# ============================================

model = load_model()

# ============================================
# PREPROCESS
# ============================================

X = prepare_inference_data(

    row,

    context_service=
    context_service
)

print("\n========== PREPROCESSED FEATURES ==========\n")

print(X.T)

# ============================================
# PREDICT
# ============================================

prediction = model.predict(X)

probabilities = model.predict_proba(X)

print("\n========== MODEL OUTPUT ==========\n")

print("Prediction:")
print(prediction)

print("\nProbabilities:")
print(probabilities)