from src.components.afiliado import Afiliado
from src.components.producto_financiero import ProductoFinanciero
from src.components.recomendacion import ResultadoCriterio
from src.services.reglas.base import ReglaProducto

PUNTOS_BASE = 10
PUNTOS_POSIBLE_CABEZA_DE_HOGAR = 5


class ReglaCreditoMujer(ReglaProducto):
    """Producto dirigido específicamente a afiliadas mujeres."""

    producto = ProductoFinanciero.CREDITO_MUJER

    def es_elegible(self, afiliado: Afiliado) -> bool:
        return afiliado.genero.strip().lower() == "mujer"

    def calcular_criterios(self, afiliado: Afiliado) -> list[ResultadoCriterio]:
        criterios = [
            ResultadoCriterio(
                puntos=PUNTOS_BASE,
                explicacion="Este producto está diseñado específicamente para afiliadas mujeres.",
            )
        ]

        convive_con_hijos_sin_pareja = (
            "Hijos" in afiliado.con_quien_vive and "Pareja" not in afiliado.con_quien_vive
        )
        if convive_con_hijos_sin_pareja:
            criterios.append(
                ResultadoCriterio(
                    puntos=PUNTOS_POSIBLE_CABEZA_DE_HOGAR,
                    explicacion=(
                        "Convive con sus hijos sin pareja registrada, un perfil "
                        "que este producto prioriza."
                    ),
                )
            )

        return criterios
