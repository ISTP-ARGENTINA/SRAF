#elaboracion del main.py
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
app = FastAPI(title="SRAF- Sistema de Registro de Activos Fijos", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def iniciar_sistema():
    inicializar()
    SistemaConfig() 
#arranca el log del singleton