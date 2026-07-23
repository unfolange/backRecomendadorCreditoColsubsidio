"""Modelos de salida del motor de recomendación."""

from dataclasses import dataclass, field

from src.components.producto_financiero import ProductoFinanciero


@dataclass(frozen=True)
class ResultadoCriterio:
    """Lo que aporta un único criterio al evaluar un producto para un afiliado."""

    puntos: float
    explicacion: str


@dataclass(frozen=True)
class Recomendacion:
    """Resultado final: qué tan recomendado está un producto y por qué."""

    producto: ProductoFinanciero
    elegible: bool
    puntaje: float
    razones: tuple[str, ...] = field(default_factory=tuple)
