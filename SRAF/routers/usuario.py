from fastapi import APIRouter, HTTPException
from dao.usuario_dao import UsuarioDAO
from schemas.usuario_schema import UsuarioCrear, UsuarioActualizar, UsuarioCambiarEstado
from config.sistema_config import UsuarioDuplicadoError, UsuarioNoEncontradoError, UsuarioConMovimientosError

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
dao = UsuarioDAO()


@router.post("", status_code=201)
def crear_usuario(datos: UsuarioCrear):
    from modelos.usuario import Usuario
    try:
        usuario = Usuario(
            datos.nombres, datos.apellidos, datos.nombre_usuario,
            datos.correo, datos.contrasena, datos.rol,
        )
        return dao.registrar(usuario).to_dict()
    except UsuarioDuplicadoError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
def listar_usuarios():
    return [u.to_dict() for u in dao.obtener_todos()]


@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: int):
    usuario = dao.buscar_por_id(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"No se encontro el usuario con ID={id_usuario}")
    return usuario.to_dict()


@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, datos: UsuarioActualizar):
    try:
        return dao.actualizar(id_usuario, datos.nombres, datos.apellidos, datos.correo, datos.rol).to_dict()
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioDuplicadoError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{id_usuario}/estado")
def cambiar_estado_usuario(id_usuario: int, datos: UsuarioCambiarEstado):
    try:
        return dao.cambiar_estado(id_usuario, datos.estado).to_dict()
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id_usuario}", status_code=204)
def eliminar_usuario(id_usuario: int):
    try:
        dao.eliminar(id_usuario)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioConMovimientosError as e:
        raise HTTPException(status_code=409, detail=str(e))
