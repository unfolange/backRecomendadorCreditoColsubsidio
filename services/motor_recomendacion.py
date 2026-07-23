"""Motor de recomendación: aplica las reglas de producto a un afiliado
y devuelve solo los productos elegibles, ordenados de más a menos
recomendado."""

from src.components.afiliado import Afiliado
from src.components.recomendacion import Recomendacion
from src.services.reglas import REGLAS_ACTIVAS
from src.services.reglas.base import ReglaProducto


class MotorRecomendacion:
    def __init__(self, reglas: tuple[ReglaProducto, ...] = REGLAS_ACTIVAS):
        self._reglas = reglas

    def recomendar_para_afiliado(self, afiliado: Afiliado) -> list[Recomendacion]:
        recomendaciones = [regla.evaluar(afiliado) for regla in self._reglas]
        elegibles = [recomendacion for recomendacion in recomendaciones if recomendacion.elegible]
        return sorted(elegibles, key=lambda recomendacion: recomendacion.puntaje, reverse=True)

    def recomendar_para_lote(
        self, afiliados: list[Afiliado]
    ) -> dict[str, list[Recomendacion]]:
        return {
            afiliado.id_afiliado: self.recomendar_para_afiliado(afiliado)
            for afiliado in afiliados
        }
