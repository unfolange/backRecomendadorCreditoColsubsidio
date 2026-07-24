"""Calcula la afinidad (0 a 100) de cada producto financiero elegible
para un afiliado, combinando dos señales:

1. El puntaje de las reglas de crédito de siempre (services/reglas),
   normalizado sobre el puntaje máximo teórico de cada regla.
2. Si el afiliado ya usó, dentro de Colsubsidio, el servicio de
   'Créditos' que corresponde a ese producto (hoja 'Servicios
   utilizados'). Es una relación que ya existe en los datos -el nombre
   del subservicio coincide con el del producto financiero-, no una
   regla de negocio inventada. Un uso real confirma interés, así que
   suma puntos extra (con tope en 100).
"""

from components.afiliado import Afiliado
from components.afinidad_producto import AfinidadProducto
from components.producto_financiero import ProductoFinanciero
from components.recomendacion import Recomendacion
from services.motor_recomendacion import MotorRecomendacion
from services.reglas import REGLAS_ACTIVAS
from services.repositorio_uso_servicios import RepositorioUsoServicios

BONUS_POR_USO_SERVICIO_RELACIONADO = 20

# Cada producto financiero activo corresponde, por nombre, a un
# subservicio real dentro de la categoría "Créditos" de la hoja
# 'Servicios utilizados'.
MAPEO_PRODUCTO_A_SERVICIO_USADO: dict[ProductoFinanciero, tuple[str, str]] = {
    ProductoFinanciero.CUPO_DE_CREDITO: ("Créditos", "Cupo de crédito / consumo rotativo"),
    ProductoFinanciero.CREDITO_HIPOTECARIO: ("Créditos", "Crédito hipotecario"),
    ProductoFinanciero.CREDITO_EDUCATIVO: ("Créditos", "Crédito educativo"),
    ProductoFinanciero.CREDITO_MUJER: ("Créditos", "Crédito Mujer"),
}


class CalculadoraAfinidadProductos:
    def __init__(
        self,
        motor: MotorRecomendacion,
        repositorio_uso_servicios: RepositorioUsoServicios,
    ):
        self._motor = motor
        self._repo_uso = repositorio_uso_servicios
        self._maximo_por_producto = {
            regla.producto: regla.puntaje_maximo for regla in REGLAS_ACTIVAS
        }

    def calcular_para_afiliado(self, afiliado: Afiliado) -> list[AfinidadProducto]:
        recomendaciones = self._motor.recomendar_para_afiliado(afiliado)
        servicios_usados = (
            self._repo_uso.servicios_usados_por(afiliado.id_afiliado)
            if self._repo_uso.tiene_historial(afiliado.id_afiliado)
            else set()
        )

        resultados = [
            self._calcular_afinidad(recomendacion, servicios_usados)
            for recomendacion in recomendaciones
        ]
        resultados.sort(key=lambda r: r.afinidad, reverse=True)
        return resultados

    def _calcular_afinidad(
        self, recomendacion: Recomendacion, servicios_usados: set[tuple[str, str]]
    ) -> AfinidadProducto:
        maximo = self._maximo_por_producto[recomendacion.producto]
        afinidad_por_reglas = min(recomendacion.puntaje / maximo, 1.0) * 100
        razones = list(recomendacion.razones)

        servicio_relacionado = MAPEO_PRODUCTO_A_SERVICIO_USADO.get(recomendacion.producto)
        ya_lo_uso = servicio_relacionado is not None and servicio_relacionado in servicios_usados

        if ya_lo_uso:
            afinidad_final = min(afinidad_por_reglas + BONUS_POR_USO_SERVICIO_RELACIONADO, 100)
            razones.append(
                "Además, ya usó este servicio dentro de Colsubsidio, lo que confirma "
                "un interés real y no solo potencial."
            )
        else:
            afinidad_final = afinidad_por_reglas

        return AfinidadProducto(
            producto=recomendacion.producto,
            afinidad=round(afinidad_final, 1),
            razones=tuple(razones),
        )
