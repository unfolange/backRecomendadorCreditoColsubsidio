"""Funciones para leer y limpiar la hoja 'Servicios utilizados' del
Excel de afiliados, servicios y canales.

Cada fila del origen es un evento: un afiliado usó un subservicio en una
fecha. Un mismo afiliado puede aparecer varias veces (usó el mismo
servicio en fechas distintas, o usó varios servicios distintos).
"""

from pathlib import Path

import pandas as pd

NOMBRE_HOJA_USO = "Servicios utilizados"

COLUMNAS_ESPERADAS = {"ID Afiliado", "Fecha de uso", "Servicio que usa", "Subservicio"}

COLUMNAS_RENOMBRADAS = {
    "ID Afiliado": "id_afiliado",
    "Fecha de uso": "fecha_uso",
    "Servicio que usa": "servicio",
    "Subservicio": "subservicio",
}


def leer_uso_servicios(ruta_excel: str | Path) -> pd.DataFrame:
    """Lee la hoja de uso de servicios y devuelve un registro por evento,
    con columnas: id_afiliado, fecha_uso, servicio, subservicio."""
    df = pd.read_excel(ruta_excel, sheet_name=NOMBRE_HOJA_USO)

    columnas_faltantes = COLUMNAS_ESPERADAS - set(df.columns)
    if columnas_faltantes:
        raise ValueError(
            f"La hoja '{NOMBRE_HOJA_USO}' no tiene las columnas esperadas: {columnas_faltantes}"
        )

    df = df.rename(columns=COLUMNAS_RENOMBRADAS)
    for columna in ("id_afiliado", "servicio", "subservicio"):
        df[columna] = df[columna].str.strip()

    return df[["id_afiliado", "fecha_uso", "servicio", "subservicio"]]
