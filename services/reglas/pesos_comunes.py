"""Pesos compartidos entre varias reglas, para no duplicarlos.

La Categoría A/B/C es la categoría de afiliación de Colsubsidio por
rango salarial (A = menor ingreso, C = mayor ingreso), confirmada como
proxy de capacidad de pago para estos productos.
"""

PUNTOS_POR_CATEGORIA: dict[str, float] = {
    "A": 5,
    "B": 10,
    "C": 15,
}


def puntos_por_categoria(categoria: str) -> float:
    return PUNTOS_POR_CATEGORIA.get(categoria.strip().upper(), 0)
