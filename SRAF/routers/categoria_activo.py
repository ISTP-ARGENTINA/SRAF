# routers/categoria_activo.py
from fastapi import APIRouter, HTTPException
from dao.categoria_activo_dao import CategoriaActivoDAO
from schemas.categoria_activo_schema import CategoriaActivoCrear, CategoriaActivoActualizar
from config.sistema_config import (
    CategoriaDuplicadaError,
    CategoriaNoEncontradaError,
    CategoriaConActivosError,
)

router = APIRouter(prefix="/categorias", tags=["Categorias de Activo"])
dao = CategoriaActivoDAO()


@router.post("", status_code=201)
def crear_categoria(datos: CategoriaActivoCrear):
    from modelos.categoria_activo import CategoriaActivo
    try:
        categoria = CategoriaActivo(datos.nombre, datos.descripcion)
        return dao.insertar(categoria).to_dict()
    except CategoriaDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_categorias():
    return [c.to_dict() for c in dao.obtener_todos()]


@router.get("/{id_categoria}")
def obtener_categoria(id_categoria: int):
    categoria = dao.buscar_por_id(id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail=f"No se encontro la categoria con ID={id_categoria}")
    return categoria.to_dict()


@router.put("/{id_categoria}")
def actualizar_categoria(id_categoria: int, datos: CategoriaActivoActualizar):
    try:
        return dao.actualizar(id_categoria, datos.nombre, datos.descripcion).to_dict()
    except CategoriaNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoriaDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{id_categoria}", status_code=204)
def eliminar_categoria(id_categoria: int):
    try:
        dao.eliminar(id_categoria)
    except CategoriaNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoriaConActivosError as e:
        raise HTTPException(status_code=409, detail=str(e))
