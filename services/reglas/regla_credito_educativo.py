from components.afiliado import Afiliado
from components.producto_financiero import ProductoFinanciero
from components.recomendacion import ResultadoCriterio
from services.reglas.base import ReglaProducto
from services.reglas.pesos_comunes import puntos_por_categoria

PUNTOS_POR_HIJO = 5


class ReglaCreditoEducativo(ReglaProducto):
    """Aplica a afiliados con hijos a cargo, que son quienes tendrían una
    necesidad de financiar educación."""

    producto = ProductoFinanciero.CREDITO_EDUCATIVO

    def es_elegible(self, afiliado: Afiliado) -> bool:
        return afiliado.tiene_hijos

    def calcular_criterios(self, afiliado: Afiliado) -> list[ResultadoCriterio]:
        return [
            ResultadoCriterio(
                puntos=afiliado.numero_hijos * PUNTOS_POR_HIJO,
                explicacion=(
                    f"Tiene {afiliado.numero_hijos} hijo(s) a cargo, la razón "
                    "principal para considerar un crédito educativo."
                ),
            ),
            ResultadoCriterio(
                puntos=puntos_por_categoria(afiliado.categoria),
                explicacion=(
                    f"Su categoría de afiliación ({afiliado.categoria}) es un "
                    "factor adicional de capacidad de pago."
                ),
            ),
        ]
