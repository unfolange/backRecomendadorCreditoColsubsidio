"""Motor de recomendación de servicios: filtrado colaborativo basado en
usuario ("user-based collaborative filtering").

Idea central: dos afiliados son "parecidos" si usan servicios parecidos
(no se mira edad, ingresos, etc. — solo comportamiento de uso, que es la
señal que pide este recomendador). Para un afiliado dado:

1. Se calcula qué tan parecido es a cada otro afiliado, comparando qué
   servicios usa cada uno (similitud coseno sobre la matriz binaria de
   uso).
2. Se toman sus K vecinos más parecidos.
3. Se sugieren los servicios que esos vecinos usan y él todavía no.

El puntaje (0 a 100) es el porcentaje ponderado de esos vecinos que usa
cada servicio candidato: una medida directa e intuitiva de qué tan
respaldada está la recomendación por perfiles similares.
"""

import numpy as np
import pandas as pd

from components.recomendacion_servicio import RecomendacionServicio
from services.repositorio_uso_servicios import RepositorioUsoServicios

CANTIDAD_VECINOS = 20
TOP_N_POR_DEFECTO = 5

MENSAJE_SIN_HISTORIAL = (
    "Este afiliado no tiene ningún registro en 'Servicios utilizados', por lo "
    "que no fue posible comparar su comportamiento con el de otros afiliados. "
    "Se muestran en su lugar los servicios más usados en general."
)

MENSAJE_SIN_VECINOS = (
    "No se encontraron afiliados con un perfil de uso parecido para comparar."
)


class RecomendadorServicios:
    def __init__(
        self,
        repositorio: RepositorioUsoServicios,
        cantidad_vecinos: int = CANTIDAD_VECINOS,
    ):
        self._repo = repositorio
        self._k = cantidad_vecinos

    def recomendar_para_afiliado(
        self, id_afiliado: str, top_n: int = TOP_N_POR_DEFECTO
    ) -> tuple[list[RecomendacionServicio], bool, str | None]:
        """Devuelve (recomendaciones, tiene_historial_de_uso, mensaje)."""
        if not self._repo.tiene_historial(id_afiliado):
            return self._recomendar_por_popularidad(top_n), False, MENSAJE_SIN_HISTORIAL

        vecinos = self._vecinos_mas_similares(id_afiliado)
        if vecinos.empty:
            return [], True, MENSAJE_SIN_VECINOS

        return self._recomendar_por_vecinos(id_afiliado, vecinos, top_n), True, None

    def _vecinos_mas_similares(self, id_afiliado: str) -> pd.Series:
        """Similitud coseno entre el afiliado y todos los demás, a partir
        de la matriz binaria de uso. 1.0 = usan exactamente los mismos
        servicios; 0.0 = ningún servicio en común."""
        matriz = self._repo.matriz
        valores = matriz.to_numpy(dtype=float)
        vector_objetivo = matriz.loc[id_afiliado].to_numpy(dtype=float)

        norma_objetivo = np.linalg.norm(vector_objetivo)
        if norma_objetivo == 0:
            return pd.Series(dtype=float)

        normas = np.linalg.norm(valores, axis=1)
        productos_punto = valores @ vector_objetivo
        with np.errstate(divide="ignore", invalid="ignore"):
            similitudes = np.where(
                normas > 0, productos_punto / (normas * norma_objetivo), 0.0
            )

        vecinos = pd.Series(similitudes, index=matriz.index).drop(index=id_afiliado)
        vecinos = vecinos[vecinos > 0]
        return vecinos.sort_values(ascending=False).head(self._k)

    def _recomendar_por_vecinos(
        self, id_afiliado: str, vecinos: pd.Series, top_n: int
    ) -> list[RecomendacionServicio]:
        usados = self._repo.servicios_usados_por(id_afiliado)
        matriz_vecinos = self._repo.matriz.loc[vecinos.index]
        peso_total = vecinos.sum()
        cantidad_vecinos = len(vecinos)

        candidatos = []
        for clave in matriz_vecinos.columns:
            if clave in usados:
                continue

            usan_este = matriz_vecinos[clave] == 1
            peso_positivo = vecinos[usan_este].sum()
            if peso_positivo <= 0:
                continue

            servicio, subservicio = clave
            cuantos = int(usan_este.sum())
            puntaje = round(float(peso_positivo / peso_total) * 100, 1)
            candidatos.append(
                RecomendacionServicio(
                    servicio=servicio,
                    subservicio=subservicio,
                    puntaje=puntaje,
                    explicacion=(
                        f"{cuantos} de los {cantidad_vecinos} afiliados con un perfil de "
                        "uso más parecido al tuyo también usan este servicio."
                    ),
                )
            )

        candidatos.sort(key=lambda r: r.puntaje, reverse=True)
        return candidatos[:top_n]

    def _recomendar_por_popularidad(self, top_n: int) -> list[RecomendacionServicio]:
        populares = self._repo.popularidad_global()[:top_n]
        return [
            RecomendacionServicio(
                servicio=servicio,
                subservicio=subservicio,
                puntaje=round(porcentaje, 1),
                explicacion=(
                    f"Es uno de los servicios más usados en general: lo usa el "
                    f"{porcentaje:.0f}% de los afiliados que sí tienen historial de uso "
                    f"registrado ({cantidad} afiliados)."
                ),
            )
            for servicio, subservicio, porcentaje, cantidad in populares
        ]
