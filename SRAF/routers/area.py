from fastapi import APIRouter, HTTPException
from dao.area_dao import AreaDAO
from schemas.area_schema import AreaCrear, AreaActualizar
from config.sistema_config import AreaDuplicadaError, AreaNoEncontradaError, AreaConActivosError

router = APIRouter(prefix="/areas", tags=["Areas"])
dao = AreaDAO()


@router.post("", status_code=201)
def crear_area(datos: AreaCrear):
    from modelos.area import Area
    try:
        area = Area(datos.nombre, datos.descripcion)
        return dao.insertar(area).to_dict()
    except AreaDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_areas():
    return [a.to_dict() for a in dao.obtener_todos()]


@router.get("/{id_area}")
def obtener_area(id_area: int):
    area = dao.buscar_por_id(id_area)
    if not area:
        raise HTTPException(status_code=404, detail=f"No se encontro el area con ID={id_area}")
    return area.to_dict()


@router.put("/{id_area}")
def actualizar_area(id_area: int, datos: AreaActualizar):
    try:
        return dao.actualizar(id_area, datos.nombre, datos.descripcion).to_dict()
    except AreaNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AreaDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{id_area}", status_code=204)
def eliminar_area(id_area: int):
    try:
        dao.eliminar(id_area)
    except AreaNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AreaConActivosError as e:
        raise HTTPException(status_code=409, detail=str(e))
