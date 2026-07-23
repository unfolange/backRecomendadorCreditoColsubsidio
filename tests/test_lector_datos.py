from src.utils.lector_datos import (
    parsear_con_quien_vive,
    parsear_ingresos,
    parsear_numero_hijos,
    parsear_tiene_mascotas,
)


def test_parsear_ingresos_quita_simbolo_y_puntos():
    assert parsear_ingresos("$6.365.000") == 6_365_000


def test_parsear_numero_hijos_valor_numerico():
    assert parsear_numero_hijos("3") == 3


def test_parsear_numero_hijos_mas_de_cuatro():
    assert parsear_numero_hijos("Más de 4") == 5


def test_parsear_con_quien_vive_separa_por_punto_y_coma():
    assert parsear_con_quien_vive("Pareja; Hijos") == ("Pareja", "Hijos")


def test_parsear_tiene_mascotas_si():
    assert parsear_tiene_mascotas("Sí") is True


def test_parsear_tiene_mascotas_no():
    assert parsear_tiene_mascotas("No") is False
