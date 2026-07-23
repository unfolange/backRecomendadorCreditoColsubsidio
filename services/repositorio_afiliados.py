"""Acceso a los datos de afiliados (Repository pattern).

Aísla al resto del sistema de cómo y dónde viven los datos. Hoy es un
CSV en memoria; si más adelante se cambia a una base de datos, solo
esta clase debería modificarse.
"""

from pathlib import Path

from components.afiliado import Afiliado
from utils.lector_datos import cargar_afiliados


class RepositorioAfiliados:
    def __init__(self, ruta_csv: str | Path):
        self._afiliados_por_id: dict[str, Afiliado] = {
            afiliado.id_afiliado: afiliado for afiliado in cargar_afiliados(ruta_csv)
        }

    def listar_todos(self) -> list[Afiliado]:
        return list(self._afiliados_por_id.values())

    def buscar_por_id(self, id_afiliado: str) -> Afiliado | None:
        return self._afiliados_por_id.get(id_afiliado.strip())

    def buscar_por_ids(
        self, ids_afiliado: list[str]
    ) -> tuple[list[Afiliado], list[str]]:
        """Devuelve (encontrados, ids_no_encontrados)."""
        encontrados: list[Afiliado] = []
        no_encontrados: list[str] = []
        for id_afiliado in ids_afiliado:
            afiliado = self.buscar_por_id(id_afiliado)
            if afiliado is None:
                no_encontrados.append(id_afiliado)
            else:
                encontrados.append(afiliado)
        return encontrados, no_encontrados
