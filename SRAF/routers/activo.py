# routers/activo.py
from fastapi import APIRouter, HTTPException
from dao.activo_dao import ActivoDAO
from dao.categoria_activo_dao import CategoriaActivoDAO
from dao.proveedor_dao import ProveedorDAO
from dao.sede_dao import SedeDAO
from dao.area_dao import AreaDAO
from schemas.activo_schema import ActivoCrear, ActivoActualizar, ActivoCambiarEstado
from config.sistema_config import (
    ActivoNoEncontradoError,
    CodigoPatrimonialDuplicadoError,
    SerieDuplicadaError,
    ActivoConDependenciasError,
    CategoriaNoEncontradaError,
    ProveedorNoEncontradoError,
    SedeNoEncontradaError,
    AreaNoEncontradaError,
)

router = APIRouter(prefix="/activos", tags=["Activos"])
dao = ActivoDAO(CategoriaActivoDAO(), ProveedorDAO(), SedeDAO(), AreaDAO())


@router.post("", status_code=201)
def crear_activo(datos: ActivoCrear):
    from modelos.activo import Activo
    try:
        activo = Activo(
            datos.codigo_patrimonial, datos.descripcion, datos.marca, datos.modelo, datos.serie,
            datos.tipo_comprobante, datos.serie_comprobante, datos.numero_comprobante, datos.fecha_compra,
            datos.valor_compra, datos.id_categoria, datos.numero_documento_proveedor, datos.id_sede, datos.id_area,
        )
        return dao.insertar(activo).to_dict()
    except (CategoriaNoEncontradaError, ProveedorNoEncontradoError, SedeNoEncontradaError, AreaNoEncontradaError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CodigoPatrimonialDuplicadoError, SerieDuplicadaError) as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_activos(id_sede: int = None, id_area: int = None):
    if id_sede is not None:
        return [a.to_dict() for a in dao.obtener_por_sede(id_sede)]
    if id_area is not None:
        return [a.to_dict() for a in dao.obtener_por_area(id_area)]
    return [a.to_dict() for a in dao.obtener_todos()]


@router.get("/{id_activo}")
def obtener_activo(id_activo: int):
    activo = dao.buscar_por_id(id_activo)
    if not activo:
        raise HTTPException(status_code=404, detail=f"No se encontro el activo con ID={id_activo}")
    return activo.to_dict()


@router.put("/{id_activo}")
def actualizar_activo(id_activo: int, datos: ActivoActualizar):
    try:
        return dao.actualizar(
            id_activo, datos.descripcion, datos.marca, datos.modelo, datos.serie,
            datos.id_categoria, datos.numero_documento_proveedor, datos.id_sede, datos.id_area,
        ).to_dict()
    except ActivoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CategoriaNoEncontradaError, ProveedorNoEncontradoError, SedeNoEncontradaError, AreaNoEncontradaError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SerieDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{id_activo}/estado")
def cambiar_estado_activo(id_activo: int, datos: ActivoCambiarEstado):
    try:
        return dao.cambiar_estado(id_activo, datos.estado).to_dict()
    except ActivoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id_activo}", status_code=204)
def eliminar_activo(id_activo: int):
    try:
        dao.eliminar(id_activo)
    except ActivoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ActivoConDependenciasError as e:
        raise HTTPException(status_code=409, detail=str(e))
