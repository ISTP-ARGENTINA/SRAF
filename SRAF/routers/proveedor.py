# routers/proveedor.py
from fastapi import APIRouter, HTTPException
from dao.proveedor_dao import ProveedorDAO
from schemas.proveedor_schema import ProveedorCrear, ProveedorActualizar
from config.sistema_config import ProveedorDuplicadoError, ProveedorNoEncontradoError, ProveedorConActivosError

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])
dao = ProveedorDAO()


@router.post("", status_code=201)
def crear_proveedor(datos: ProveedorCrear):
    from modelos.proveedor import Proveedor
    try:
        proveedor = Proveedor(
            datos.numero_documento_proveedor, datos.tipo_documento,
            datos.razon_social, datos.telefono, datos.correo,
        )
        return dao.insertar(proveedor).to_dict()
    except ProveedorDuplicadoError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_proveedores():
    return [p.to_dict() for p in dao.obtener_todos()]


@router.get("/{numero_documento_proveedor}")
def obtener_proveedor(numero_documento_proveedor: str):
    proveedor = dao.buscar_por_id(numero_documento_proveedor.upper())
    if not proveedor:
        raise HTTPException(status_code=404, detail=f"No se encontro el proveedor con documento '{numero_documento_proveedor}'")
    return proveedor.to_dict()


@router.put("/{numero_documento_proveedor}")
def actualizar_proveedor(numero_documento_proveedor: str, datos: ProveedorActualizar):
    try:
        return dao.actualizar(
            numero_documento_proveedor.upper(), datos.tipo_documento,
            datos.razon_social, datos.telefono, datos.correo,
        ).to_dict()
    except ProveedorNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{numero_documento_proveedor}", status_code=204)
def eliminar_proveedor(numero_documento_proveedor: str):
    try:
        dao.eliminar(numero_documento_proveedor.upper())
    except ProveedorNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProveedorConActivosError as e:
        raise HTTPException(status_code=409, detail=str(e))
