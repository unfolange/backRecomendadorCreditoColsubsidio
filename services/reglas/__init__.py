"""Registro central de las reglas de producto activas.

Para agregar un producto nuevo: crear su clase `ReglaProducto` en este
paquete y añadirla a `REGLAS_ACTIVAS`. Nada más necesita cambiar.
"""

from services.reglas.base import ReglaProducto
from services.reglas.regla_credito_educativo import ReglaCreditoEducativo
from services.reglas.regla_credito_hipotecario import ReglaCreditoHipotecario
from services.reglas.regla_credito_mujer import ReglaCreditoMujer
from services.reglas.regla_cupo_credito import ReglaCupoDeCredito

REGLAS_ACTIVAS: tuple[ReglaProducto, ...] = (
    ReglaCupoDeCredito(),
    ReglaCreditoHipotecario(),
    ReglaCreditoEducativo(),
    ReglaCreditoMujer(),
)
