import pandas as pd


def clean(df):
    """Limpia el dataset Online Retail y devuelve una copia procesada."""

    df = df.copy()

    # 1. Eliminar filas completamente duplicadas.
    df = df.drop_duplicates()

    # 2. Eliminar registros sin descripción del producto.
    # Sin Description no podemos identificar correctamente el artículo.
    df = df.dropna(subset=["Description"])

    # 3. Normalizar las columnas de texto.
    df["Description"] = (
        df["Description"]
        .astype("string")
        .str.strip()
    )

    df["Country"] = (
        df["Country"]
        .astype("string")
        .str.strip()
    )

    # 4. Eliminar posibles descripciones nulas que permanezcan
    # después de la normalización.
    df = df.dropna(subset=["Description"])

    # 5. Mantener Customer ID nulo cuando el cliente
    # no puede ser identificado.
    df["Customer ID"] = df["Customer ID"].astype("Int64")

    # 6. Asegurar el tipo fecha.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # 7. Eliminar precios negativos.
    # Los casos detectados correspondían a ajustes contables
    # ("Adjust bad debt"), no a ventas de productos.
    df = df[df["Price"] >= 0]

    return df