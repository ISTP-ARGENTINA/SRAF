# routers/baja_activo.py
from fastapi import APIRouter, HTTPException
from dao.baja_activo_dao import BajaActivoDAO
from dao.activo_dao import ActivoDAO
from dao.categoria_activo_dao import CategoriaActivoDAO
from dao.prooveedor_dao import ProveedorDAO
from dao.sede_dao import SedeDAO
from dao.area_dao import AreaDAO
from dao.usuario_dao import UsuarioDAO
from schemas.baja_activo_schema import BajaActivoCrear
from config.sistema_config import (
    BajaNoEncontradaError,
    ActivoYaDadoDeBajaError,
    ActivoNoEncontradoError,
    UsuarioNoEncontradoError,
)

router = APIRouter(prefix="/bajas", tags=["Bajas de Activo"])
_activo_dao = ActivoDAO(CategoriaActivoDAO(), ProveedorDAO(), SedeDAO(), AreaDAO())
dao = BajaActivoDAO(_activo_dao, UsuarioDAO())


@router.post("", status_code=201)
def crear_baja(datos: BajaActivoCrear):
    from modelos.baja_activo import BajaActivo
    try:
        baja = BajaActivo(datos.motivo, datos.descripcion, datos.id_activo, datos.id_usuario)
        return dao.insertar(baja).to_dict()
    except (ActivoNoEncontradoError, UsuarioNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ActivoYaDadoDeBajaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_bajas():
    return [b.to_dict() for b in dao.obtener_todos()]


@router.get("/{id_baja}")
def obtener_baja(id_baja: int):
    baja = dao.buscar_por_id(id_baja)
    if not baja:
        raise HTTPException(status_code=404, detail=f"No se encontro la baja con ID={id_baja}")
    return baja.to_dict()

