"""Registro central de las reglas de producto activas.

Para agregar un producto nuevo: crear su clase `ReglaProducto` en este
paquete y añadirla a `REGLAS_ACTIVAS`. Nada más necesita cambiar.
"""

from src.services.reglas.base import ReglaProducto
from src.services.reglas.regla_credito_educativo import ReglaCreditoEducativo
from src.services.reglas.regla_credito_hipotecario import ReglaCreditoHipotecario
from src.services.reglas.regla_credito_mujer import ReglaCreditoMujer
from src.services.reglas.regla_cupo_credito import ReglaCupoDeCredito

REGLAS_ACTIVAS: tuple[ReglaProducto, ...] = (
    ReglaCupoDeCredito(),
    ReglaCreditoHipotecario(),
    ReglaCreditoEducativo(),
    ReglaCreditoMujer(),
)
