# routers/ajuste_activo.py
from fastapi import APIRouter, HTTPException
from dao.ajuste_activo_dao import AjusteActivoDAO
from dao.activo_dao import ActivoDAO
from dao.categoria_activo_dao import CategoriaActivoDAO
from dao.proveedor_dao import ProveedorDAO
from dao.sede_dao import SedeDAO
from dao.area_dao import AreaDAO
from dao.usuario_dao import UsuarioDAO
from schemas.ajuste_activo_schema import AjusteActivoCrear
from config.sistema_config import AjusteNoEncontradoError, ActivoNoEncontradoError, UsuarioNoEncontradoError

router = APIRouter(prefix="/ajustes", tags=["Ajustes de Activo"])
_activo_dao = ActivoDAO(CategoriaActivoDAO(), ProveedorDAO(), SedeDAO(), AreaDAO())
dao = AjusteActivoDAO(_activo_dao, UsuarioDAO())


@router.post("", status_code=201)
def crear_ajuste(datos: AjusteActivoCrear):
    from modelos.ajuste_activo import AjusteActivo
    try:
        ajuste = AjusteActivo(
            datos.tipo_ajuste, datos.valor_anterior, datos.valor_nuevo,
            datos.observacion, datos.id_activo, datos.id_usuario,
        )
        return dao.insertar(ajuste).to_dict()
    except (ActivoNoEncontradoError, UsuarioNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("")
def listar_ajustes(id_activo: int = None):
    if id_activo is not None:
        return [a.to_dict() for a in dao.obtener_por_activo(id_activo)]
    return [a.to_dict() for a in dao.obtener_todos()]


@router.get("/{id_ajuste}")
def obtener_ajuste(id_ajuste: int):
    ajuste = dao.buscar_por_id(id_ajuste)
    if not ajuste:
        raise HTTPException(status_code=404, detail=f"No se encontro el ajuste con ID={id_ajuste}")
    return ajuste.to_dict()


@router.delete("/{id_ajuste}", status_code=204)
def eliminar_ajuste(id_ajuste: int):
    try:
        dao.eliminar(id_ajuste)
    except AjusteNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
