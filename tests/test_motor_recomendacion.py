from components.producto_financiero import ProductoFinanciero
from services.motor_recomendacion import MotorRecomendacion


def test_solo_devuelve_productos_elegibles(crear_afiliado):
    afiliado = crear_afiliado(
        genero="Hombre", numero_hijos=0, tipo_vivienda="Propia", antiguedad_anios=5
    )
    recomendaciones = MotorRecomendacion().recomendar_para_afiliado(afiliado)
    productos = {r.producto for r in recomendaciones}

    assert ProductoFinanciero.CUPO_DE_CREDITO in productos
    assert ProductoFinanciero.CREDITO_HIPOTECARIO not in productos
    assert ProductoFinanciero.CREDITO_EDUCATIVO not in productos
    assert ProductoFinanciero.CREDITO_MUJER not in productos


def test_resultados_ordenados_de_mayor_a_menor_puntaje(crear_afiliado):
    afiliado = crear_afiliado(
        genero="Mujer",
        numero_hijos=2,
        tipo_vivienda="Arriendo",
        antiguedad_anios=8,
        categoria="C",
    )
    recomendaciones = MotorRecomendacion().recomendar_para_afiliado(afiliado)

    puntajes = [r.puntaje for r in recomendaciones]
    assert puntajes == sorted(puntajes, reverse=True)


def test_cada_recomendacion_incluye_al_menos_una_razon(crear_afiliado):
    afiliado = crear_afiliado(genero="Mujer", numero_hijos=1, tipo_vivienda="Arriendo")
    recomendaciones = MotorRecomendacion().recomendar_para_afiliado(afiliado)

    assert recomendaciones
    for recomendacion in recomendaciones:
        assert len(recomendacion.razones) > 0


def test_recomendar_para_lote_devuelve_una_entrada_por_afiliado(crear_afiliado):
    afiliados = [
        crear_afiliado(id_afiliado="AF-1", antiguedad_anios=2),
        crear_afiliado(id_afiliado="AF-2", antiguedad_anios=0),
    ]
    resultado = MotorRecomendacion().recomendar_para_lote(afiliados)

    assert set(resultado.keys()) == {"AF-1", "AF-2"}
