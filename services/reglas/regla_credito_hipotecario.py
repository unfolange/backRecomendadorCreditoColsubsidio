from components.afiliado import Afiliado
from components.producto_financiero import ProductoFinanciero
from components.recomendacion import ResultadoCriterio
from services.reglas.base import ReglaProducto
from services.reglas.pesos_comunes import puntos_por_categoria

ANTIGUEDAD_TOPE_PARA_PUNTAJE = 10
EDAD_LIMITE_PARA_PLAZO_LARGO = 55


class ReglaCreditoHipotecario(ReglaProducto):
    """Aplica a quien todavía no tiene vivienda propia. El puntaje prioriza
    a quienes ya muestran capacidad de pago y margen de tiempo para un
    plazo hipotecario largo."""

    producto = ProductoFinanciero.CREDITO_HIPOTECARIO

    def es_elegible(self, afiliado: Afiliado) -> bool:
        return not afiliado.vive_en_vivienda_propia

    def calcular_criterios(self, afiliado: Afiliado) -> list[ResultadoCriterio]:
        antiguedad_para_puntaje = min(afiliado.antiguedad_anios, ANTIGUEDAD_TOPE_PARA_PUNTAJE)
        criterios = [
            ResultadoCriterio(
                puntos=0,
                explicacion=(
                    f"Actualmente vive en una vivienda de tipo '{afiliado.tipo_vivienda}', "
                    "no es propietario(a)."
                ),
            ),
            ResultadoCriterio(
                puntos=puntos_por_categoria(afiliado.categoria) * 2,
                explicacion=(
                    f"Su categoría de afiliación ({afiliado.categoria}) respalda "
                    "un compromiso financiero de largo plazo."
                ),
            ),
            ResultadoCriterio(
                puntos=antiguedad_para_puntaje * 2,
                explicacion=(
                    f"Lleva {afiliado.antiguedad_anios} año(s) como afiliado, lo "
                    "que aporta estabilidad."
                ),
            ),
        ]

        if afiliado.edad <= EDAD_LIMITE_PARA_PLAZO_LARGO:
            criterios.append(
                ResultadoCriterio(
                    puntos=10,
                    explicacion=(
                        f"Su edad ({afiliado.edad} años) permite completar un "
                        "plazo hipotecario largo."
                    ),
                )
            )
        else:
            criterios.append(
                ResultadoCriterio(
                    puntos=2,
                    explicacion=(
                        f"A su edad ({afiliado.edad} años) aún puede acceder a "
                        "hipotecas con plazos más cortos."
                    ),
                )
            )

        return criterios
