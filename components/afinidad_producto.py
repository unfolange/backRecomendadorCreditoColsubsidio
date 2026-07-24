"""Modelo de salida del cálculo de afinidad de productos financieros."""

from dataclasses import dataclass, field

from components.producto_financiero import ProductoFinanciero


@dataclass(frozen=True)
class AfinidadProducto:
    """Qué tan afín es un producto financiero para un afiliado (0 a 100),
    combinando las reglas de crédito con el uso real de servicios."""

    producto: ProductoFinanciero
    afinidad: float
    razones: tuple[str, ...] = field(default_factory=tuple)
