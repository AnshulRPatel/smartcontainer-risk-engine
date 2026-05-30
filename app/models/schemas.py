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

    risk_label: str

    model_confidence: float

    risk_score: float

    anomaly_score: float

    explanation: str

class HealthResponse(BaseModel):

    status: str

    service: str

    api_version: str

    timestamp: str

    model_loaded: bool

class ReadyResponse(BaseModel):

    ready: bool

class ModelInfoResponse(BaseModel):

    model_name: str

    model_version: str

    api_version: str

    framework: str

    task: str

    target_classes: list[str]

    features_count: int

    features: list[str]