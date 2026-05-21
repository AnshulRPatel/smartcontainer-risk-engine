TARGET_COLUMN = "Risk_Label"

RANDOM_STATE = 42

TEST_SIZE = 0.2


# =========================
# EXPERIMENT TRACKING
# =========================

MODEL_NAME = "CatBoost"

EXPERIMENT_PHASE = "no_importer_behavior_v3"

EXPERIMENT_NAME = (
    f"customs_risk_{MODEL_NAME.lower()}"
)


# =========================
# MODEL STORAGE
# =========================

MODEL_PATH = (
    "outputs/models/catboost_risk_model.cbm"
)


# =========================
# FEATURE ENGINEERING STRATEGY
# =========================

ENABLE_ANOMALY_FEATURES = True

ENABLE_BEHAVIORAL_FEATURES = True

ENABLE_TEMPORAL_FEATURES = True

ENABLE_LOG_FEATURES = True

ENABLE_CORRELATION_PRUNING = False


# =========================
# CORRELATION SETTINGS
# =========================

CORRELATION_THRESHOLD = 0.90


# =========================
# CATBOOST PARAMETERS
# =========================

CATBOOST_PARAMS = {

    "iterations": 500,

    "learning_rate": 0.05,

    "depth": 6,

    "loss_function": "MultiClass",

    "eval_metric": "TotalF1",

    "random_seed": RANDOM_STATE,

    "verbose": 100,

    "auto_class_weights": "Balanced"
}