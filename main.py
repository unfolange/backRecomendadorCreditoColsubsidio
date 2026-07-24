"""Punto de entrada de la API.

Arquitectura: Frontend -> API FastAPI -> Motor de recomendación -> JSON.
Este archivo solo traduce HTTP <-> dominio; toda la lógica de negocio
vive en src/services.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    AfinidadesProductosAfiliadoSchema,
    AfinidadProductoSchema,
    RecomendacionesAfiliadoSchema,
    RecomendacionesLoteSchema,
    RecomendacionesServiciosAfiliadoSchema,
    RecomendacionSchema,
    RecomendacionServicioSchema,
)
from services.calculadora_afinidad_productos import CalculadoraAfinidadProductos
from services.motor_recomendacion import MotorRecomendacion
from services.recomendador_servicios import TOP_N_POR_DEFECTO, RecomendadorServicios
from services.repositorio_afiliados import RepositorioAfiliados
from services.repositorio_uso_servicios import RepositorioUsoServicios
from utils.lector_ids import leer_ids_desde_archivo

RUTA_CSV_AFILIADOS = (
    Path(__file__).resolve().parent
    / "data"
    / "Afiliados_Sinteticos_Colsubsidio_2000(Afiliados).csv"
)
RUTA_EXCEL_SERVICIOS = (
    Path(__file__).resolve().parent
    / "data"
    / "Afiliados_Servicios_y_Canales_Sinteticos_Colsubsidio.xlsx"
)

app = FastAPI(
    title="Recomendador de Productos Financieros Colsubsidio",
    description=(
        "Recomienda productos financieros de Colsubsidio a partir del "
        "perfil de un afiliado, explicando cada recomendación. No aprueba "
        "ni rechaza créditos."
    ),
    version="0.1.0",
)

# Permite que el front (servido desde otro origen) consuma esta API.
# Se abre a todos los orígenes porque durante la hackatón el front puede
# desplegarse en distintas URLs y no se conoce una lista fija de antemano.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

repositorio = RepositorioAfiliados(RUTA_CSV_AFILIADOS)
motor = MotorRecomendacion()

repositorio_uso_servicios = RepositorioUsoServicios(RUTA_EXCEL_SERVICIOS)
recomendador_servicios = RecomendadorServicios(repositorio_uso_servicios)
calculadora_afinidad_productos = CalculadoraAfinidadProductos(motor, repositorio_uso_servicios)


@app.get("/afiliados/{id_afiliado}/recomendaciones", response_model=RecomendacionesAfiliadoSchema)
def recomendar_para_un_afiliado(id_afiliado: str) -> RecomendacionesAfiliadoSchema:
    afiliado = repositorio.buscar_por_id(id_afiliado)
    if afiliado is None:
        raise HTTPException(status_code=404, detail=f"Afiliado '{id_afiliado}' no encontrado.")

    recomendaciones = motor.recomendar_para_afiliado(afiliado)
    return RecomendacionesAfiliadoSchema(
        id_afiliado=afiliado.id_afiliado,
        nombre=afiliado.nombre,
        recomendaciones=[RecomendacionSchema.desde_dominio(r) for r in recomendaciones],
    )


@app.post("/afiliados/recomendaciones/lote", response_model=RecomendacionesLoteSchema)
async def recomendar_para_lote(archivo: UploadFile) -> RecomendacionesLoteSchema:
    contenido = await archivo.read()
    try:
        ids_afiliado = leer_ids_desde_archivo(contenido, archivo.filename or "")
    except Exception as error:
        raise HTTPException(
            status_code=400, detail=f"No se pudo leer el archivo: {error}"
        ) from error

    if not ids_afiliado:
        raise HTTPException(status_code=400, detail="El archivo no contiene identificadores.")

    afiliados, no_encontrados = repositorio.buscar_por_ids(ids_afiliado)
    recomendaciones_por_afiliado = motor.recomendar_para_lote(afiliados)

    resultados = [
        RecomendacionesAfiliadoSchema(
            id_afiliado=afiliado.id_afiliado,
            nombre=afiliado.nombre,
            recomendaciones=[
                RecomendacionSchema.desde_dominio(r)
                for r in recomendaciones_por_afiliado[afiliado.id_afiliado]
            ],
        )
        for afiliado in afiliados
    ]

    return RecomendacionesLoteSchema(resultados=resultados, ids_no_encontrados=no_encontrados)


@app.get(
    "/afiliados/{id_afiliado}/servicios-recomendados",
    response_model=RecomendacionesServiciosAfiliadoSchema,
)
def recomendar_servicios_para_un_afiliado(
    id_afiliado: str, top_n: int = TOP_N_POR_DEFECTO
) -> RecomendacionesServiciosAfiliadoSchema:
    afiliado = repositorio.buscar_por_id(id_afiliado)
    if afiliado is None:
        raise HTTPException(status_code=404, detail=f"Afiliado '{id_afiliado}' no encontrado.")

    recomendaciones, tiene_historial_uso, mensaje = recomendador_servicios.recomendar_para_afiliado(
        afiliado.id_afiliado, top_n=top_n
    )
    return RecomendacionesServiciosAfiliadoSchema(
        id_afiliado=afiliado.id_afiliado,
        nombre=afiliado.nombre,
        tiene_historial_uso=tiene_historial_uso,
        mensaje=mensaje,
        recomendaciones=[RecomendacionServicioSchema.desde_dominio(r) for r in recomendaciones],
    )


@app.get(
    "/afiliados/{id_afiliado}/afinidad-productos",
    response_model=AfinidadesProductosAfiliadoSchema,
)
def afinidad_productos_para_un_afiliado(id_afiliado: str) -> AfinidadesProductosAfiliadoSchema:
    afiliado = repositorio.buscar_por_id(id_afiliado)
    if afiliado is None:
        raise HTTPException(status_code=404, detail=f"Afiliado '{id_afiliado}' no encontrado.")

    productos = calculadora_afinidad_productos.calcular_para_afiliado(afiliado)
    return AfinidadesProductosAfiliadoSchema(
        id_afiliado=afiliado.id_afiliado,
        nombre=afiliado.nombre,
        productos=[AfinidadProductoSchema.desde_dominio(p) for p in productos],
    )
