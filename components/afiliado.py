"""Entidad de dominio que representa a un afiliado de Colsubsidio."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Afiliado:
    """Perfil de un afiliado, ya limpio y tipado (sin formatos de texto crudo)."""

    id_afiliado: str
    nombre: str
    edad: int
    ingresos: int
    antiguedad_anios: int
    categoria: str
    departamento: str
    ciudad: str
    numero_hijos: int
    con_quien_vive: tuple[str, ...] = field(default_factory=tuple)
    tipo_vivienda: str = ""
    tipo_suelo: str = ""
    estado_civil: str = ""
    genero: str = ""
    tiene_mascotas: bool = False

    @property
    def tiene_hijos(self) -> bool:
        return self.numero_hijos > 0

    @property
    def vive_en_vivienda_propia(self) -> bool:
        return self.tipo_vivienda.strip().lower() == "propia"
