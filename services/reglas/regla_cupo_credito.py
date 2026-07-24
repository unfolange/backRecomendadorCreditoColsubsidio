from components.afiliado import Afiliado
from components.producto_financiero import ProductoFinanciero
from components.recomendacion import ResultadoCriterio
from services.reglas.base import ReglaProducto
from services.reglas.pesos_comunes import puntos_por_categoria

ANTIGUEDAD_MINIMA_ANIOS = 1
ANTIGUEDAD_TOPE_PARA_PUNTAJE = 10


class ReglaCupoDeCredito(ReglaProducto):
    """El cupo de crédito es el producto base: solo pide una afiliación
    mínimamente estable. El puntaje ordena a quién conviene ofrecerlo primero."""

    producto = ProductoFinanciero.CUPO_DE_CREDITO

    # antigüedad tope (10 años * 2) + categoría máxima (C = 15).
    puntaje_maximo = ANTIGUEDAD_TOPE_PARA_PUNTAJE * 2 + 15

    def es_elegible(self, afiliado: Afiliado) -> bool:
        return afiliado.antiguedad_anios >= ANTIGUEDAD_MINIMA_ANIOS

    def calcular_criterios(self, afiliado: Afiliado) -> list[ResultadoCriterio]:
        antiguedad_para_puntaje = min(afiliado.antiguedad_anios, ANTIGUEDAD_TOPE_PARA_PUNTAJE)
        return [
            ResultadoCriterio(
                puntos=antiguedad_para_puntaje * 2,
                explicacion=(
                    f"Lleva {afiliado.antiguedad_anios} año(s) como afiliado, "
                    "lo que da estabilidad para un cupo de crédito."
                ),
            ),
            ResultadoCriterio(
                puntos=puntos_por_categoria(afiliado.categoria),
                explicacion=(
                    f"Su categoría de afiliación ({afiliado.categoria}) respalda "
                    "su capacidad de pago."
                ),
            ),
        ]
