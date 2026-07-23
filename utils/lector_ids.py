"""Lee una lista de IDs de afiliado desde un archivo CSV o Excel subido
por el usuario (consulta masiva)."""

import io

import pandas as pd

NOMBRES_DE_COLUMNA_ACEPTADOS = ("ID Afiliado", "id afiliado", "Cédula", "cedula", "Cedula")


def _elegir_columna_de_ids(columnas: list[str]) -> str:
    for nombre in NOMBRES_DE_COLUMNA_ACEPTADOS:
        if nombre in columnas:
            return nombre
    return columnas[0]


def leer_ids_desde_archivo(contenido: bytes, nombre_archivo: str) -> list[str]:
    if nombre_archivo.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(contenido), dtype=str)
    else:
        df = pd.read_csv(io.BytesIO(contenido), dtype=str, sep=None, engine="python")

    if df.empty:
        return []

    columna = _elegir_columna_de_ids(list(df.columns))
    return [valor.strip() for valor in df[columna].dropna().astype(str) if valor.strip()]
