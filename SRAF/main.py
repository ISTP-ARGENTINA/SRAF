from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config.base_datos import inicializar
from config.sistema_config import SistemaConfig

from routers import (
    categoria_activo,
    proveedor,
    sede,
    area,
    usuario,
    inventario_fisico,
    activo,
    ajuste_activo,
    baja_activo,
    detalle_inventario,
)

app = FastAPI(title="SRAF - Sistema de Registro de Activos Fijos", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def iniciar_sistema():
    inicializar()
    SistemaConfig()  # dispara el log de arranque del singleton


# Convierte los errores de validacion de Pydantic (422) en un formato
# simple y legible para el frontend.
@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, exc: RequestValidationError):
    errores = [
        {"campo": ".".join(str(p) for p in err["loc"][1:]), "mensaje": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": errores})


app.include_router(categoria_activo.router)
app.include_router(proveedor.router)
app.include_router(sede.router)
app.include_router(area.router)
app.include_router(usuario.router)
app.include_router(inventario_fisico.router)
app.include_router(activo.router)
app.include_router(ajuste_activo.router)
app.include_router(baja_activo.router)
app.include_router(detalle_inventario.router)


@app.get("/")
def raiz():
    return {"mensaje": "API Sistema de Registro de Activos Fijos (SRAF)", "version": "1.0", "docs": "/docs"}