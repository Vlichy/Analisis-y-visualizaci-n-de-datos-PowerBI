from pathlib import Path
import pandas as pd


def load_excel(file_path, sheet_name="Year 2010-2011"):
    """Carga una hoja de un archivo Excel y devuelve un DataFrame."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {file_path}"
        )

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

    return df


def export_csv(df, file_path):
    """Exporta un DataFrame a CSV sin guardar el índice."""

    file_path = Path(file_path)

    # Creamos la carpeta de destino si no existe.
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Exportamos el dataset procesado.
    df.to_csv(
        file_path,
        index=False
    )

    print(
        f"Dataset exportado correctamente en: {file_path}"
    )