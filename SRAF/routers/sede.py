from fastapi import APIRouter, HTTPException
from dao.sede_dao import SedeDAO
from schemas.sede_schema import SedeCrear, SedeActualizar
from config.sistema_config import SedeDuplicadaError, SedeNoEncontradaError, SedeConActivosError

router = APIRouter(prefix="/sedes", tags=["Sedes"])
dao = SedeDAO()


@router.post("", status_code=201)
def crear_sede(datos: SedeCrear):
    from modelos.sede import Sede
    try:
        sede = Sede(datos.nombre, datos.direccion, datos.ciudad)
        return dao.insertar(sede).to_dict()
    except SedeDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_sedes():
    return [s.to_dict() for s in dao.obtener_todos()]


@router.get("/{id_sede}")
def obtener_sede(id_sede: int):
    sede = dao.buscar_por_id(id_sede)
    if not sede:
        raise HTTPException(status_code=404, detail=f"No se encontro la sede con ID={id_sede}")
    return sede.to_dict()


@router.put("/{id_sede}")
def actualizar_sede(id_sede: int, datos: SedeActualizar):
    try:
        return dao.actualizar(id_sede, datos.nombre, datos.direccion, datos.ciudad).to_dict()
    except SedeNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SedeDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{id_sede}", status_code=204)
def eliminar_sede(id_sede: int):
    try:
        dao.eliminar(id_sede)
    except SedeNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SedeConActivosError as e:
        raise HTTPException(status_code=409, detail=str(e))

