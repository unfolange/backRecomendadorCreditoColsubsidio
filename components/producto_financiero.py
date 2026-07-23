"""Catálogo de productos financieros de Colsubsidio."""

from enum import Enum


class ProductoFinanciero(str, Enum):
    CUPO_DE_CREDITO = "Cupo de crédito"
    CREDITO_HIPOTECARIO = "Crédito hipotecario"
    CREDITO_EDUCATIVO = "Crédito educativo"
    COMPRA_DE_CARTERA = "Compra de cartera"
    CREDITO_MUJER = "Crédito Mujer"
    CREDITO_COMPLEMENTARIO = "Crédito complementario"
    CREDITO_ROTATIVO_SEGUROS_IMPUESTOS = "Crédito rotativo para seguros e impuestos"


# Productos para los que aún no existe una señal confiable en los datos
# disponibles (p. ej. requieren historial de deudas o de créditos vigentes).
# Se documentan aquí para que el motor de recomendación los omita a propósito,
# en vez de generar una recomendación basada en una suposición.
PRODUCTOS_PENDIENTES_DE_DATOS: frozenset[ProductoFinanciero] = frozenset(
    {
        ProductoFinanciero.COMPRA_DE_CARTERA,
        ProductoFinanciero.CREDITO_COMPLEMENTARIO,
        ProductoFinanciero.CREDITO_ROTATIVO_SEGUROS_IMPUESTOS,
    }
)
