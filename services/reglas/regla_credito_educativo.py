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

    # número de hijos máximo real en los datos ("Más de 4" se trata como
    # 5, ver utils/lector_datos.py) * puntos por hijo (5*5=25) +
    # categoría máxima (15).
    NUMERO_HIJOS_MAXIMO_EN_DATOS = 5
    puntaje_maximo = NUMERO_HIJOS_MAXIMO_EN_DATOS * PUNTOS_POR_HIJO + 15

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
