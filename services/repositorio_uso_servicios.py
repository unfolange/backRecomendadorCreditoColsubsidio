"""Acceso a los datos de uso de servicios (Repository pattern).

Construye, a partir de la hoja 'Servicios utilizados', la matriz binaria
afiliado x (servicio, subservicio) que usa el recomendador de servicios
para medir similitud entre perfiles.

Se usa la pareja (servicio, subservicio) como clave -en vez de solo el
subservicio- porque un mismo nombre de subservicio puede repetirse bajo
categorías distintas (p. ej. "D'parche" existe tanto en "Cultura y
entretenimiento" como en "Comunidades"). Mezclarlos sería inventar una
relación que los datos no confirman.
"""

from pathlib import Path

import pandas as pd

from utils.lector_servicios import leer_uso_servicios


class RepositorioUsoServicios:
    def __init__(self, ruta_excel: str | Path):
        df = leer_uso_servicios(ruta_excel)
        self._matriz = self._construir_matriz(df)

    @classmethod
    def desde_dataframe(cls, df: pd.DataFrame) -> "RepositorioUsoServicios":
        """Construye el repositorio a partir de un DataFrame ya en memoria
        (columnas: id_afiliado, fecha_uso, servicio, subservicio).

        Pensado para pruebas: evita depender de un archivo Excel real.
        """
        instancia = cls.__new__(cls)
        instancia._matriz = cls._construir_matriz(df)
        return instancia

    @staticmethod
    def _construir_matriz(df: pd.DataFrame) -> pd.DataFrame:
        conteos = pd.pivot_table(
            df,
            index="id_afiliado",
            columns=["servicio", "subservicio"],
            values="fecha_uso",
            aggfunc="count",
            fill_value=0,
        )
        # Solo interesa si el afiliado usó el servicio alguna vez, no cuántas veces.
        return (conteos > 0).astype(int)

    @property
    def matriz(self) -> pd.DataFrame:
        return self._matriz

    def tiene_historial(self, id_afiliado: str) -> bool:
        return id_afiliado in self._matriz.index

    def servicios_usados_por(self, id_afiliado: str) -> set[tuple[str, str]]:
        fila = self._matriz.loc[id_afiliado]
        return {clave for clave, usado in fila.items() if usado == 1}

    def popularidad_global(self) -> list[tuple[str, str, float, int]]:
        """(servicio, subservicio, % de afiliados con historial que lo usan,
        cantidad de afiliados), ordenado de más a menos popular."""
        total_con_historial = len(self._matriz.index)
        conteos = self._matriz.sum(axis=0)
        porcentajes = (conteos / total_con_historial) * 100

        resultado = [
            (servicio, subservicio, float(porcentajes[(servicio, subservicio)]), int(conteo))
            for (servicio, subservicio), conteo in conteos.items()
        ]
        resultado.sort(key=lambda item: item[2], reverse=True)
        return resultado
