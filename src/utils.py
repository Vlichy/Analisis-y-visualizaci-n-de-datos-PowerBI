def validate_columns(df, required_columns):
    """
    Comprueba que el DataFrame contiene todas las columnas necesarias.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Faltan columnas obligatorias: {missing_columns}"
        )


def print_data_summary(df):
    """
    Muestra un resumen básico del estado del dataset.
    """

    print("\n=== RESUMEN DEL DATASET ===")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")
    print(f"Duplicados: {df.duplicated().sum()}")

    print("\nValores nulos por columna:")
    print(df.isnull().sum())


def validate_processed_data(df):
    """
    Realiza comprobaciones básicas sobre el dataset procesado.
    """

    required_columns = [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
        "TotalAmount",
        "IsCancelled",
        "Year",
        "Month",
        "MonthName",
        "DayOfWeek",
        "Hour",
    ]

    validate_columns(df, required_columns)

    # Después de la limpieza no deberían quedar precios negativos.
    if (df["Price"] < 0).any():
        raise ValueError(
            "El dataset procesado todavía contiene precios negativos."
        )

    # Después de la limpieza no deberían quedar descripciones nulas.
    if df["Description"].isnull().any():
        raise ValueError(
            "El dataset procesado contiene descripciones nulas."
        )

    print(
        "\nValidación del dataset procesado completada correctamente."
    )