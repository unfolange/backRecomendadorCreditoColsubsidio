"""Contrato común para toda regla de producto (patrón Strategy).

Cada producto financiero es una clase independiente que implementa esta
interfaz. El motor de recomendación no conoce los detalles de ningún
producto: solo sabe que puede llamar a `evaluar(afiliado)`. Agregar un
producto nuevo significa crear una clase nueva, sin tocar el motor.
"""

from abc import ABC, abstractmethod

from src.components.afiliado import Afiliado
from src.components.producto_financiero import ProductoFinanciero
from src.components.recomendacion import Recomendacion, ResultadoCriterio


class ReglaProducto(ABC):
    producto: ProductoFinanciero

    @abstractmethod
    def es_elegible(self, afiliado: Afiliado) -> bool:
        """Condición determinante: si no se cumple, el producto no aplica."""

    @abstractmethod
    def calcular_criterios(self, afiliado: Afiliado) -> list[ResultadoCriterio]:
        """Puntos y explicaciones que ordenan la fuerza de la recomendación."""

    def evaluar(self, afiliado: Afiliado) -> Recomendacion:
        elegible = self.es_elegible(afiliado)
        criterios = self.calcular_criterios(afiliado) if elegible else []
        return Recomendacion(
            producto=self.producto,
            elegible=elegible,
            puntaje=sum(criterio.puntos for criterio in criterios),
            razones=tuple(criterio.explicacion for criterio in criterios),
        )
