"""Modelo de salida del recomendador de servicios."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RecomendacionServicio:
    """Un servicio sugerido para un afiliado, con su puntaje de afinidad
    (0 a 100) y la razón por la que se sugiere."""

    servicio: str
    subservicio: str
    puntaje: float
    explicacion: str
