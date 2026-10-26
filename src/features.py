import pandas as pd


def build_features(df):
    """Construye variables derivadas para el análisis."""

    df = df.copy()

    # Importe de cada línea
    df["TotalAmount"] = df["Quantity"] * df["Price"]

    # Identificar facturas canceladas
    df["IsCancelled"] = (
        df["Invoice"]
        .astype(str)
        .str.startswith("C")
    )

    # Variables temporales
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.month_name()
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    df["Hour"] = df["InvoiceDate"].dt.hour

    return df