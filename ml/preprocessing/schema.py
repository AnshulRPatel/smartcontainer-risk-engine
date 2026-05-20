EXPECTED_COLUMNS = {
    "Container_ID": "int64",
    "Declaration_Date": "datetime64[ns]",
    "Declaration_Time": "object",
    "Trade_Regime": "object",
    "Origin_Country": "object",
    "Destination_Country": "object",
    "Destination_Port": "object",
    "HS_Code": "object",
    "Importer_ID": "object",
    "Exporter_ID": "object",
    "Declared_Value": "float64",
    "Declared_Weight": "float64",
    "Measured_Weight": "float64",
    "Shipping_Line": "object",
    "Dwell_Time_Hours": "float64",
    "Clearance_Status": "object"
}

VALID_TRADE_REGIMES = [
    "Import",
    "Export",
    "Transit"
]

VALID_CLEARANCE_STATUS = [
    "Cleared",
    "Pending",
    "Inspection",
    "Rejected"
]