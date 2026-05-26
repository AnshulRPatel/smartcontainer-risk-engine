import pandas as pd

from app.services.anomaly_service import (
    anomaly_service
)


class ContextService:

    def __init__(self):

        # =================================================
        # LOAD REFERENCE DATASET
        # =================================================

        self.reference_data = pd.read_csv(
            "data/processed/anomaly_shipments.csv"
        )

        # =================================================
        # LOAD REAL ANOMALY SERVICE
        # =================================================

        self.anomaly_service = (
            anomaly_service
        )

    # =====================================================
    # EXPORTER HISTORY
    # =====================================================

    def get_exporter_shipment_count(

        self,

        exporter_id
    ):

        count = (

            self.reference_data[
                self.reference_data[
                    "Exporter_ID"
                ]
                == exporter_id
            ]

            .shape[0]
        )

        return max(count, 1)

    # =====================================================
    # SHIPPING LINE FREQUENCY
    # =====================================================

    def get_shipping_line_frequency(

        self,

        shipping_line
    ):

        count = (

            self.reference_data[
                self.reference_data[
                    "Shipping_Line"
                ]
                == shipping_line
            ]

            .shape[0]
        )

        return max(count, 1)

    # =====================================================
    # IMPORTER HISTORY
    # =====================================================

    def get_importer_shipment_count(

        self,

        importer_id
    ):

        count = (

            self.reference_data[
                self.reference_data[
                    "Importer_ID"
                ]
                == importer_id
            ]

            .shape[0]
        )

        return max(count, 1)

    # =====================================================
    # ROUTE RISK ESTIMATION
    # =====================================================

    def estimate_route_risk(

        self,

        origin_country,

        destination_country
    ):

        risky_routes = [

            ("CN", "IN"),

            ("AE", "IN"),

            ("SG", "IN")
        ]

        if (

            origin_country,

            destination_country

        ) in risky_routes:

            return 1

        return 0

    # =====================================================
    # HIGH RISK PORT CHECK
    # =====================================================

    def is_high_risk_port(

        self,

        destination_port
    ):

        high_risk_ports = [

            "PORT_40",

            "PORT_77",

            "PORT_12"
        ]

        return int(
            destination_port
            in high_risk_ports
        )

    # =====================================================
    # REFERENCE LOOKUP
    # =====================================================

    def get_reference_statistics(self):

        return {

            "total_shipments": (

                self.reference_data
                .shape[0]
            ),

            "high_risk_ratio": (

                self.reference_data[
                    "Risk_Label"
                ]
                .value_counts(
                    normalize=True
                )
                .to_dict()
            )
        }


# =========================================================
# SINGLETON INSTANCE
# =========================================================

context_service = ContextService()