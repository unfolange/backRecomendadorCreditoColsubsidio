import pandas as pd
import pytest

from services.recomendador_servicios import RecomendadorServicios
from services.repositorio_uso_servicios import RepositorioUsoServicios


def _fila(id_afiliado, servicio, subservicio, fecha="2024-01-01"):
    return {
        "id_afiliado": id_afiliado,
        "fecha_uso": fecha,
        "servicio": servicio,
        "subservicio": subservicio,
    }


@pytest.fixture
def repo_pequeno():
    """AF-1, AF-2 y AF-3 tienen perfiles de uso parecidos (Gimnasios +
    Piscilago). AF-2 y AF-3 además usan Vitalito, que AF-1 todavía no usa:
    esa es la recomendación esperada. AF-4 no se parece a nadie."""
    filas = [
        _fila("AF-1", "Deportes", "Gimnasios"),
        _fila("AF-1", "Turismo", "Piscilago"),
        _fila("AF-2", "Deportes", "Gimnasios"),
        _fila("AF-2", "Turismo", "Piscilago"),
        _fila("AF-2", "Salud", "Vitalito"),
        _fila("AF-3", "Deportes", "Gimnasios"),
        _fila("AF-3", "Turismo", "Piscilago"),
        _fila("AF-3", "Salud", "Vitalito"),
        _fila("AF-4", "Cultura y entretenimiento", "Teatro Colsubsidio"),
    ]
    return RepositorioUsoServicios.desde_dataframe(pd.DataFrame(filas))


def test_recomienda_lo_que_usan_los_vecinos_mas_parecidos(repo_pequeno):
    motor = RecomendadorServicios(repo_pequeno)
    recomendaciones, tiene_historial, mensaje = motor.recomendar_para_afiliado("AF-1")

    assert tiene_historial is True
    assert mensaje is None
    subservicios = {r.subservicio for r in recomendaciones}
    assert "Vitalito" in subservicios
    assert "Teatro Colsubsidio" not in subservicios


def test_no_recomienda_servicios_ya_usados(repo_pequeno):
    motor = RecomendadorServicios(repo_pequeno)
    recomendaciones, _, _ = motor.recomendar_para_afiliado("AF-1")

    subservicios = {r.subservicio for r in recomendaciones}
    assert "Gimnasios" not in subservicios
    assert "Piscilago" not in subservicios


def test_puntajes_normalizados_entre_0_y_100(repo_pequeno):
    motor = RecomendadorServicios(repo_pequeno)
    recomendaciones, _, _ = motor.recomendar_para_afiliado("AF-1")

    assert recomendaciones
    for recomendacion in recomendaciones:
        assert 0 <= recomendacion.puntaje <= 100


def test_afiliado_sin_historial_usa_popularidad_y_lo_advierte(repo_pequeno):
    motor = RecomendadorServicios(repo_pequeno)
    recomendaciones, tiene_historial, mensaje = motor.recomendar_para_afiliado("AF-999")

    assert tiene_historial is False
    assert mensaje is not None
    assert "no tiene ningún registro" in mensaje
    assert "Servicios utilizados" in mensaje
    assert recomendaciones
    subservicios_top = {r.subservicio for r in recomendaciones[:2]}
    assert "Gimnasios" in subservicios_top
