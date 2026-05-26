import json

from pathlib import Path

class RiskCalibrationService:

    def __init__(self):

        threshold_file = Path(
            "outputs/artifacts/risk_thresholds.json"
        )

        if not threshold_file.exists():

            raise FileNotFoundError(

                "Risk threshold file not found.\n"
                "Run build_labels.py first."
            )

        with open(

            threshold_file,

            "r"
        ) as f:

            thresholds = json.load(f)

        self.value_threshold_95 = (

            thresholds[
                "value_threshold_95"
            ]
        )

        self.value_threshold_99 = (

            thresholds[
                "value_threshold_99"
            ]
        )

        self.dwell_threshold_95 = (

            thresholds[
                "dwell_threshold_95"
            ]
        )

        self.importer_threshold_10 = (

            thresholds[
                "importer_threshold_10"
            ]
        )

        print(
            "\nLoaded Risk Thresholds:"
        )

        print(
            thresholds
        )

    # ==============================================
    # MAIN RISK CALCULATION
    # ==============================================

    def calculate_operational_risk(

        self,

        declared_value,

        weight_diff_percent,

        dwell_time,

        importer_count,

        is_night_declaration,

        was_zero_declared_weight,

        was_zero_declared_value,

        route_risk_score
    ):

        # ==========================================
        # WEIGHT RISK
        # ==========================================

        if abs(weight_diff_percent) > 50:

            weight_risk = 3

        elif abs(weight_diff_percent) > 20:

            weight_risk = 2

        else:

            weight_risk = 0

        # ==========================================
        # VALUE RISK
        # ==========================================

        if declared_value > self.value_threshold_99:

            value_risk = 3

        elif declared_value > self.value_threshold_95:

            value_risk = 2

        else:

            value_risk = 0

        # ==========================================
        # DWELL RISK
        # ==========================================

        dwell_risk = (

            2

            if dwell_time >
            self.dwell_threshold_95

            else 0
        )

        # ==========================================
        # BEHAVIORAL RISK
        # ==========================================

        behavioral_risk = (

            3

            if importer_count <
            self.importer_threshold_10

            else 0
        )

        # ==========================================
        # TEMPORAL RISK
        # ==========================================

        temporal_risk = (

            2

            if is_night_declaration == 1

            else 0
        )

        # ==========================================
        # INTEGRITY RISK
        # ==========================================

        integrity_risk = (

            3

            if (

                was_zero_declared_weight

                +

                was_zero_declared_value

            ) > 0

            else 0
        )

        # ==========================================
        # NORMALIZATION
        # ==========================================

        normalized_weight = (
            weight_risk / 3
        )

        normalized_value = (
            value_risk / 3
        )

        normalized_dwell = (
            dwell_risk / 2
        )

        normalized_route = (
            route_risk_score / 2
        )

        normalized_behavioral = (
            behavioral_risk / 3
        )

        normalized_temporal = (
            temporal_risk / 2
        )

        normalized_integrity = (
            integrity_risk / 3
        )

        # ==========================================
        # FINAL SCORE
        # ==========================================

        total_risk_score = (

            0.30 * normalized_weight

            +

            0.25 * normalized_value

            +

            0.20 * normalized_dwell

            +

            0.10 * normalized_route

            +

            0.10 * normalized_behavioral

            +

            0.03 * normalized_temporal

            +

            0.02 * normalized_integrity
        )

        return round(
            float(total_risk_score),
            3
        )


risk_calibration_service = (
    RiskCalibrationService()
)