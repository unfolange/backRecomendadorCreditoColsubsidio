from src.services.reglas.regla_credito_educativo import ReglaCreditoEducativo
from src.services.reglas.regla_credito_hipotecario import ReglaCreditoHipotecario
from src.services.reglas.regla_credito_mujer import ReglaCreditoMujer
from src.services.reglas.regla_cupo_credito import ReglaCupoDeCredito


class TestReglaCupoDeCredito:
    def test_no_elegible_si_afiliacion_muy_reciente(self, crear_afiliado):
        afiliado = crear_afiliado(antiguedad_anios=0)
        resultado = ReglaCupoDeCredito().evaluar(afiliado)
        assert resultado.elegible is False
        assert resultado.razones == ()

    def test_elegible_con_un_anio_de_antiguedad(self, crear_afiliado):
        afiliado = crear_afiliado(antiguedad_anios=1)
        resultado = ReglaCupoDeCredito().evaluar(afiliado)
        assert resultado.elegible is True
        assert resultado.puntaje > 0

    def test_mayor_categoria_da_mayor_puntaje(self, crear_afiliado):
        puntaje_a = ReglaCupoDeCredito().evaluar(crear_afiliado(categoria="A")).puntaje
        puntaje_c = ReglaCupoDeCredito().evaluar(crear_afiliado(categoria="C")).puntaje
        assert puntaje_c > puntaje_a


class TestReglaCreditoHipotecario:
    def test_no_elegible_si_ya_tiene_vivienda_propia(self, crear_afiliado):
        afiliado = crear_afiliado(tipo_vivienda="Propia")
        resultado = ReglaCreditoHipotecario().evaluar(afiliado)
        assert resultado.elegible is False

    def test_elegible_si_vive_en_arriendo(self, crear_afiliado):
        afiliado = crear_afiliado(tipo_vivienda="Arriendo")
        resultado = ReglaCreditoHipotecario().evaluar(afiliado)
        assert resultado.elegible is True

    def test_persona_mas_joven_obtiene_mas_puntos_por_plazo(self, crear_afiliado):
        joven = ReglaCreditoHipotecario().evaluar(
            crear_afiliado(tipo_vivienda="Arriendo", edad=30)
        )
        mayor = ReglaCreditoHipotecario().evaluar(
            crear_afiliado(tipo_vivienda="Arriendo", edad=60)
        )
        assert joven.puntaje > mayor.puntaje


class TestReglaCreditoEducativo:
    def test_no_elegible_sin_hijos(self, crear_afiliado):
        afiliado = crear_afiliado(numero_hijos=0)
        resultado = ReglaCreditoEducativo().evaluar(afiliado)
        assert resultado.elegible is False

    def test_mas_hijos_da_mas_puntaje(self, crear_afiliado):
        un_hijo = ReglaCreditoEducativo().evaluar(crear_afiliado(numero_hijos=1)).puntaje
        tres_hijos = ReglaCreditoEducativo().evaluar(crear_afiliado(numero_hijos=3)).puntaje
        assert tres_hijos > un_hijo


class TestReglaCreditoMujer:
    def test_no_elegible_si_no_es_mujer(self, crear_afiliado):
        afiliado = crear_afiliado(genero="Hombre")
        resultado = ReglaCreditoMujer().evaluar(afiliado)
        assert resultado.elegible is False

    def test_elegible_si_es_mujer(self, crear_afiliado):
        afiliado = crear_afiliado(genero="Mujer")
        resultado = ReglaCreditoMujer().evaluar(afiliado)
        assert resultado.elegible is True

    def test_bono_por_posible_cabeza_de_hogar(self, crear_afiliado):
        con_pareja = ReglaCreditoMujer().evaluar(
            crear_afiliado(genero="Mujer", con_quien_vive=("Pareja", "Hijos"))
        )
        sin_pareja = ReglaCreditoMujer().evaluar(
            crear_afiliado(genero="Mujer", con_quien_vive=("Hijos",))
        )
        assert sin_pareja.puntaje > con_pareja.puntaje
