import pandas as pd

df = pd.read_csv(
    "data/processed/anomaly_shipments.csv"
)

print("\nVALUE THRESHOLDS")
print(df["Declared_Value"].quantile(0.95))
print(df["Declared_Value"].quantile(0.99))

print("\nDWELL THRESHOLD")
print(df["Dwell_Time_Hours"].quantile(0.95))

print("\nIMPORTER THRESHOLD")
print(df["Importer_Shipment_Count"].quantile(0.10))