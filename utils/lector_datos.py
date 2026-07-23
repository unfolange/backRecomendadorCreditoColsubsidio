"""Funciones para leer y limpiar el CSV de afiliados.

El archivo fuente viene con formato "humano" (moneda con $ y puntos,
texto separado por ';', etc.). Aquí se concentra toda esa limpieza para
que el resto del sistema trabaje siempre con tipos de datos simples.
"""

from pathlib import Path

import pandas as pd

from src.components.afiliado import Afiliado

# El archivo fue exportado con codificación Latin-1 y separador ';'.
CODIFICACION_CSV = "latin-1"
SEPARADOR_CSV = ";"

COLUMNAS_ESPERADAS = {
    "ID Afiliado",
    "Nombre Afiliado",
    "Edad",
    "Ingresos",
    "Antigüedad como afiliado (años)",
    "Categoría",
    "Departamento",
    "Ciudad",
    "Número de hijos",
    "Con quien vive",
    "Tipo de vivienda",
    "Tipo de suelo",
    "Estado civil",
    "Género",
    "Tiene Mascotas",
}


def parsear_ingresos(valor: str) -> int:
    """Convierte '$6.365.000' en 6365000."""
    solo_digitos = "".join(caracter for caracter in str(valor) if caracter.isdigit())
    return int(solo_digitos) if solo_digitos else 0


def parsear_numero_hijos(valor: str) -> int:
    """Convierte '1', '0' o 'Más de 4' en un entero.

    'Más de 4' se trata como 5: es un piso razonable para efectos de
    puntaje (a mayor número de hijos, mayor puntaje), sin inventar un
    valor exacto que el dato no ofrece.
    """
    texto = str(valor).strip()
    if texto.isdigit():
        return int(texto)
    return 5


def parsear_con_quien_vive(valor: str) -> tuple[str, ...]:
    """Convierte 'Pareja; Hijos' en ('Pareja', 'Hijos')."""
    return tuple(parte.strip() for parte in str(valor).split(";") if parte.strip())


def parsear_tiene_mascotas(valor: str) -> bool:
    return str(valor).strip().lower() == "sí"


def leer_csv_afiliados(ruta_csv: str | Path) -> pd.DataFrame:
    """Lee el CSV crudo de afiliados sin transformarlo todavía."""
    df = pd.read_csv(ruta_csv, sep=SEPARADOR_CSV, encoding=CODIFICACION_CSV, dtype=str)

    columnas_faltantes = COLUMNAS_ESPERADAS - set(df.columns)
    if columnas_faltantes:
        raise ValueError(
            f"El CSV de afiliados no tiene las columnas esperadas: {columnas_faltantes}"
        )
    return df


def fila_a_afiliado(fila: pd.Series) -> Afiliado:
    """Convierte una fila del CSV (ya leída como texto) en un Afiliado tipado."""
    return Afiliado(
        id_afiliado=fila["ID Afiliado"].strip(),
        nombre=fila["Nombre Afiliado"].strip(),
        edad=int(fila["Edad"]),
        ingresos=parsear_ingresos(fila["Ingresos"]),
        antiguedad_anios=int(fila["Antigüedad como afiliado (años)"]),
        categoria=fila["Categoría"].strip(),
        departamento=fila["Departamento"].strip(),
        ciudad=fila["Ciudad"].strip(),
        numero_hijos=parsear_numero_hijos(fila["Número de hijos"]),
        con_quien_vive=parsear_con_quien_vive(fila["Con quien vive"]),
        tipo_vivienda=fila["Tipo de vivienda"].strip(),
        tipo_suelo=fila["Tipo de suelo"].strip(),
        estado_civil=fila["Estado civil"].strip(),
        genero=fila["Género"].strip(),
        tiene_mascotas=parsear_tiene_mascotas(fila["Tiene Mascotas"]),
    )


def cargar_afiliados(ruta_csv: str | Path) -> list[Afiliado]:
    """Lee el CSV completo y lo convierte en una lista de Afiliado."""
    df = leer_csv_afiliados(ruta_csv)
    return [fila_a_afiliado(fila) for _, fila in df.iterrows()]
