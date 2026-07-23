"""Esquemas Pydantic de entrada/salida de la API.

Se mantienen separados de las entidades de dominio (src/components) a
propósito: el dominio no debe depender de cómo se serializa por HTTP.
"""

from pydantic import BaseModel

from src.components.recomendacion import Recomendacion


class RecomendacionSchema(BaseModel):
    producto: str
    puntaje: float
    razones: list[str]

    @classmethod
    def desde_dominio(cls, recomendacion: Recomendacion) -> "RecomendacionSchema":
        return cls(
            producto=recomendacion.producto.value,
            puntaje=recomendacion.puntaje,
            razones=list(recomendacion.razones),
        )


class RecomendacionesAfiliadoSchema(BaseModel):
    id_afiliado: str
    nombre: str
    recomendaciones: list[RecomendacionSchema]


class RecomendacionesLoteSchema(BaseModel):
    resultados: list[RecomendacionesAfiliadoSchema]
    ids_no_encontrados: list[str]
