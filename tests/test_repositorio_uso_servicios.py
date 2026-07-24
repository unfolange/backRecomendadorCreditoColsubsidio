import pandas as pd

from services.repositorio_uso_servicios import RepositorioUsoServicios


def _fila(id_afiliado, servicio, subservicio, fecha="2024-01-01"):
    return {
        "id_afiliado": id_afiliado,
        "fecha_uso": fecha,
        "servicio": servicio,
        "subservicio": subservicio,
    }


def test_uso_repetido_del_mismo_servicio_cuenta_una_sola_vez():
    df = pd.DataFrame(
        [
            _fila("AF-1", "Salud", "Vitalito", "2024-01-01"),
            _fila("AF-1", "Salud", "Vitalito", "2024-06-01"),
        ]
    )
    repo = RepositorioUsoServicios.desde_dataframe(df)

    assert repo.servicios_usados_por("AF-1") == {("Salud", "Vitalito")}


def test_mismo_nombre_de_subservicio_en_categorias_distintas_no_se_mezcla():
    df = pd.DataFrame(
        [
            _fila("AF-1", "Cultura y entretenimiento", "D'parche"),
            _fila("AF-2", "Comunidades", "D'parche"),
        ]
    )
    repo = RepositorioUsoServicios.desde_dataframe(df)

    assert repo.servicios_usados_por("AF-1") == {("Cultura y entretenimiento", "D'parche")}
    assert repo.servicios_usados_por("AF-2") == {("Comunidades", "D'parche")}


def test_tiene_historial():
    df = pd.DataFrame([_fila("AF-1", "Salud", "Vitalito")])
    repo = RepositorioUsoServicios.desde_dataframe(df)

    assert repo.tiene_historial("AF-1") is True
    assert repo.tiene_historial("AF-999") is False


def test_popularidad_global_ordenada_de_mayor_a_menor():
    df = pd.DataFrame(
        [
            _fila("AF-1", "Salud", "Vitalito"),
            _fila("AF-2", "Salud", "Vitalito"),
            _fila("AF-3", "Deportes", "Gimnasios"),
        ]
    )
    repo = RepositorioUsoServicios.desde_dataframe(df)

    populares = repo.popularidad_global()
    assert populares[0][:2] == ("Salud", "Vitalito")
    assert populares[0][2] > populares[1][2]
