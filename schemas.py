"""Esquemas Pydantic de entrada/salida de la API.

Se mantienen separados de las entidades de dominio (src/components) a
propósito: el dominio no debe depender de cómo se serializa por HTTP.
"""

from pydantic import BaseModel

from components.afinidad_producto import AfinidadProducto
from components.recomendacion import Recomendacion
from components.recomendacion_servicio import RecomendacionServicio


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


class RecomendacionServicioSchema(BaseModel):
    servicio: str
    subservicio: str
    puntaje: float
    explicacion: str

    @classmethod
    def desde_dominio(cls, recomendacion: RecomendacionServicio) -> "RecomendacionServicioSchema":
        return cls(
            servicio=recomendacion.servicio,
            subservicio=recomendacion.subservicio,
            puntaje=recomendacion.puntaje,
            explicacion=recomendacion.explicacion,
        )


class RecomendacionesServiciosAfiliadoSchema(BaseModel):
    id_afiliado: str
    nombre: str
    tiene_historial_uso: bool
    mensaje: str | None = None
    recomendaciones: list[RecomendacionServicioSchema]


class AfinidadProductoSchema(BaseModel):
    producto: str
    afinidad: float
    razones: list[str]

    @classmethod
    def desde_dominio(cls, afinidad: AfinidadProducto) -> "AfinidadProductoSchema":
        return cls(
            producto=afinidad.producto.value,
            afinidad=afinidad.afinidad,
            razones=list(afinidad.razones),
        )


class AfinidadesProductosAfiliadoSchema(BaseModel):
    id_afiliado: str
    nombre: str
    productos: list[AfinidadProductoSchema]
