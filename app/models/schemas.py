from pydantic import BaseModel


class ShipmentInput(BaseModel):

    Container_ID: str

    Declaration_Date: str

    Declaration_Time: str

    Trade_Regime: str

    Origin_Country: str

    Destination_Port: str

    Destination_Country: str

    HS_Code: str

    Importer_ID: str

    Exporter_ID: str

    Declared_Value: float

    Declared_Weight: float

    Measured_Weight: float

    Shipping_Line: str

    Dwell_Time_Hours: float


class PredictionResponse(BaseModel):

    container_id: str

    predicted_risk: str

    risk_score: float

    anomaly_score: float

    explanation: str