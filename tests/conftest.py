import pytest

from src.components.afiliado import Afiliado


@pytest.fixture
def crear_afiliado():
    """Fábrica de Afiliado con valores por defecto razonables, para que
    cada prueba solo indique los campos que le importan."""

    def _crear(**overrides) -> Afiliado:
        valores_por_defecto = dict(
            id_afiliado="AF-000001",
            nombre="Afiliado de prueba",
            edad=35,
            ingresos=3_000_000,
            antiguedad_anios=5,
            categoria="B",
            departamento="Bogotá D.C.",
            ciudad="Bogotá D.C.",
            numero_hijos=0,
            con_quien_vive=(),
            tipo_vivienda="Arriendo",
            tipo_suelo="Urbano",
            estado_civil="Soltero",
            genero="Hombre",
            tiene_mascotas=False,
        )
        valores_por_defecto.update(overrides)
        return Afiliado(**valores_por_defecto)

    return _crear
