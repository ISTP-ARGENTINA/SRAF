# routers/inventario_fisico.py
from fastapi import APIRouter, HTTPException
from dao.inventario_fisico_dao import InventarioFisicoDAO
from schemas.inventario_fisico_schema import InventarioFisicoCrear, InventarioFisicoCerrar
from config.sistema_config import InventarioNoEncontradoError

router = APIRouter(prefix="/inventarios", tags=["Inventario Fisico"])
dao = InventarioFisicoDAO()


@router.post("", status_code=201)
def crear_inventario(datos: InventarioFisicoCrear):
    from modelos.inventario_fisico import InventarioFisico
    inventario = InventarioFisico(datos.anio)
    return dao.insertar(inventario).to_dict()


@router.get("")
def listar_inventarios():
    return [i.to_dict() for i in dao.obtener_todos()]


@router.get("/{id_inventario}")
def obtener_inventario(id_inventario: int):
    inventario = dao.buscar_por_id(id_inventario)
    if not inventario:
        raise HTTPException(status_code=404, detail=f"No se encontro el inventario fisico con ID={id_inventario}")
    return inventario.to_dict()


@router.patch("/{id_inventario}/cerrar")
def cerrar_inventario(id_inventario: int, datos: InventarioFisicoCerrar):
    try:
        return dao.cerrar(id_inventario, datos.fecha_fin).to_dict()
    except InventarioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id_inventario}", status_code=204)
def eliminar_inventario(id_inventario: int):
    try:
        dao.eliminar(id_inventario)
    except InventarioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
