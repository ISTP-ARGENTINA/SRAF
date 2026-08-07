# routers/detalle_inventario.py
from fastapi import APIRouter, HTTPException
from dao.detalle_inventario_dao import DetalleInventarioDAO
from dao.inventario_fisico_dao import InventarioFisicoDAO
from dao.activo_dao import ActivoDAO
from dao.categoria_activo_dao import CategoriaActivoDAO
from dao.prooveedor_dao import ProveedorDAO
from dao.sede_dao import SedeDAO
from dao.area_dao import AreaDAO
from schemas.detalle_inventario_schema import DetalleInventarioCrear, DetalleInventarioActualizar
from config.sistema_config import (
    DetalleNoEncontradoError,
    ActivoYaEscaneadoError,
    InventarioNoEncontradoError,
    InventarioCerradoError,
    ActivoNoEncontradoError,
)

router = APIRouter(prefix="/detalle-inventario", tags=["Detalle de Inventario"])
_activo_dao = ActivoDAO(CategoriaActivoDAO(), ProveedorDAO(), SedeDAO(), AreaDAO())
dao = DetalleInventarioDAO(InventarioFisicoDAO(), _activo_dao)


@router.post("", status_code=201)
def crear_detalle(datos: DetalleInventarioCrear):
    from modelos.detalle_inventario import DetalleInventario
    try:
        detalle = DetalleInventario(datos.id_inventario, datos.id_activo, datos.encontrado, datos.observacion)
        return dao.insertar(detalle).to_dict()
    except (InventarioNoEncontradoError, ActivoNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InventarioCerradoError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ActivoYaEscaneadoError as e:
        raise HTTPException(status_code=409, detail=str(e))