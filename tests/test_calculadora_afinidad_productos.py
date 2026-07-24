import pandas as pd
import pytest

from services.calculadora_afinidad_productos import CalculadoraAfinidadProductos
from services.motor_recomendacion import MotorRecomendacion
from services.repositorio_uso_servicios import RepositorioUsoServicios


def _fila(id_afiliado, servicio, subservicio, fecha="2024-01-01"):
    return {
        "id_afiliado": id_afiliado,
        "fecha_uso": fecha,
        "servicio": servicio,
        "subservicio": subservicio,
    }


@pytest.fixture
def repo_uso_vacio():
    return RepositorioUsoServicios.desde_dataframe(
        pd.DataFrame(columns=["id_afiliado", "fecha_uso", "servicio", "subservicio"])
    )


def test_afinidad_entre_0_y_100(crear_afiliado, repo_uso_vacio):
    afiliado = crear_afiliado(
        genero="Mujer", numero_hijos=2, tipo_vivienda="Arriendo", antiguedad_anios=8, categoria="C"
    )
    calculadora = CalculadoraAfinidadProductos(MotorRecomendacion(), repo_uso_vacio)
    afinidades = calculadora.calcular_para_afiliado(afiliado)

    assert afinidades
    for afinidad in afinidades:
        assert 0 <= afinidad.afinidad <= 100


def test_uso_real_del_servicio_relacionado_sube_la_afinidad(crear_afiliado):
    afiliado = crear_afiliado(
        id_afiliado="AF-1", tipo_vivienda="Arriendo", antiguedad_anios=1, categoria="A"
    )
    df_sin_uso = pd.DataFrame(columns=["id_afiliado", "fecha_uso", "servicio", "subservicio"])
    df_con_uso = pd.DataFrame([_fila("AF-1", "Créditos", "Crédito hipotecario")])

    calculadora_sin_uso = CalculadoraAfinidadProductos(
        MotorRecomendacion(), RepositorioUsoServicios.desde_dataframe(df_sin_uso)
    )
    calculadora_con_uso = CalculadoraAfinidadProductos(
        MotorRecomendacion(), RepositorioUsoServicios.desde_dataframe(df_con_uso)
    )

    def afinidad_hipotecario(calculadora):
        afinidades = calculadora.calcular_para_afiliado(afiliado)
        return next(a.afinidad for a in afinidades if a.producto.value == "Crédito hipotecario")

    afinidad_base = afinidad_hipotecario(calculadora_sin_uso)
    afinidad_con_bono = afinidad_hipotecario(calculadora_con_uso)

    assert afinidad_con_bono > afinidad_base
    assert afinidad_con_bono <= 100


def test_razones_mencionan_el_uso_real_cuando_aplica(crear_afiliado):
    afiliado = crear_afiliado(id_afiliado="AF-1", tipo_vivienda="Arriendo")
    df_con_uso = pd.DataFrame([_fila("AF-1", "Créditos", "Crédito hipotecario")])
    calculadora = CalculadoraAfinidadProductos(
        MotorRecomendacion(), RepositorioUsoServicios.desde_dataframe(df_con_uso)
    )

    afinidades = calculadora.calcular_para_afiliado(afiliado)
    hipotecario = next(a for a in afinidades if a.producto.value == "Crédito hipotecario")

    assert any("ya usó este servicio" in razon for razon in hipotecario.razones)


def test_afiliado_sin_historial_de_uso_no_falla(crear_afiliado, repo_uso_vacio):
    afiliado = crear_afiliado(id_afiliado="AF-999", tipo_vivienda="Arriendo")
    calculadora = CalculadoraAfinidadProductos(MotorRecomendacion(), repo_uso_vacio)

    afinidades = calculadora.calcular_para_afiliado(afiliado)
    assert afinidades
