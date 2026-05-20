def add_importer_risk_features(df):

    importer_freq = (
        df["Importer_ID"]
        .value_counts()
    )

    df["Importer_Shipment_Count"] = (
        df["Importer_ID"]
        .map(importer_freq)
    )

    return df


def add_exporter_risk_features(df):

    exporter_freq = (
        df["Exporter_ID"]
        .value_counts()
    )

    df["Exporter_Shipment_Count"] = (
        df["Exporter_ID"]
        .map(exporter_freq)
    )

    return df


def add_shipping_line_frequency(df):

    shipping_freq = (
        df["Shipping_Line"]
        .value_counts()
    )

    df["Shipping_Line_Frequency"] = (
        df["Shipping_Line"]
        .map(shipping_freq)
    )

    return df