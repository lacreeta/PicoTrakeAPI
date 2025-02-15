from fastapi import FastAPI, HTTPException, Depends
import db_suscripciones
import db_usuario
from models import *
from db import get_connection
from typing import List
from auth import *
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

app = FastAPI(debug=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Modificar Swagger para que solo pida el token JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi 


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de PicoTrake"}

# ----- Endpoints para SUSCRIPCIONES -----


@app.get("/suscripciones", response_model=List[Suscripcion])
def get_suscripciones():
    suscripciones_data = db_suscripciones.readAll()
    if not suscripciones_data:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ninguna suscripción")
    return suscripciones_data


@app.get("/suscripciones/{id_suscripcion}")
def get_suscripcion(id_suscripcion: int):
    if db_suscripciones.readById(id_suscripcion) is not None:
        suscripcion = db_suscripciones.readById(id_suscripcion)
    else:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ninguna suscripción por esta ID")
    return suscripcion


@app.post("/suscripciones")
async def create_suscripcion(suscripcion: Suscripcion):
    return db_suscripciones.create(suscripcion)


@app.put("/suscripciones/{id_suscripcion}")
def update_suscripcion(id_suscripcion: int, suscripcion: Suscripcion):
    return db_suscripciones.update(id_suscripcion, suscripcion)


@app.delete("/suscripciones/{id_suscripcion}")
def delete_suscripcion(id_suscripcion: int):
    return db_suscripciones.delete(id_suscripcion)

# ----- Endpoints para USUARIOS -----

# no usado por usuarios reales
@app.get("/usuarios")
def get_usuarios():
    usuarios_data = db_usuario.readAll()
    if not usuarios_data:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ningun usuario")
    return usuarios_data

# no usado por usuarios reales
@app.get("/usuarios/{id_usuario}")
def get_usuario(id_usuario: int):
    usuario = db_usuario.readById(id_usuario)
    if usuario is None:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ningún usuario por esta ID"
        )
    return usuario

@app.post("/usuarios")
async def create_usuario(usuario: UsuarioCreate):
    return db_usuario.create(usuario)


@app.put("/usuarios/{id_usuario}")
def update_usuario(id_usuario: int, data: UpdateUserRequest):
    data_filtrada = data.model_dump(exclude_unset=True)
    return db_usuario.update(id_usuario, data_filtrada)


@app.put("/usuarios/password/update")
def update_password_user(
    datos: UpdatePasswordRequest,
    usuario: dict = Depends(obtener_usuario_actual)
):
    print("🔹 La función `update_password_user` se ejecutó")  # DEBUG
    print(f"🔹 Usuario autenticado: {usuario}")  # DEBUG
    print(f"🔹 Datos recibidos (tipo {type(datos)}): {datos}")  # DEBUG
    id_usuario = usuario["id_usuario"]
    return db_usuario.update_password_db(id_usuario, datos.contrasena_actual, datos.nueva_contrasena)

@app.post("/login")
def login_user(login_data: LoginRequest):
    return db_usuario.login(login_data)


@app.delete("/usuarios/{id_usuario}")
def delete_usuario(id_usuario: int):
    return db_usuario.delete(id_usuario)

# ----- Endpoints para RUTAS -----


@app.get("/rutas")
def get_rutas():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM RUTAS;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rutas/{id_ruta}")
def get_ruta(id_ruta: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM RUTAS WHERE id_ruta = %s;", (id_ruta,))
        ruta = cur.fetchone()
        cur.close()
        conn.close()
        if ruta is None:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return ruta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rutas")
def create_ruta(ruta: Ruta):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO RUTAS (id_ruta, nombre_ruta, dificultad, ubicacion, descripcion)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (
            ruta.id_ruta,
            ruta.nombre_ruta,
            ruta.dificultad,
            ruta.ubicacion,
            ruta.descripcion
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Ruta creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/rutas/{id_ruta}")
def update_ruta(id_ruta: int, ruta: Ruta):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE RUTAS
            SET nombre_ruta = %s, dificultad = %s, ubicacion = %s, descripcion = %s
            WHERE id_ruta = %s;
        """
        values = (
            ruta.nombre_ruta,
            ruta.dificultad,
            ruta.ubicacion,
            ruta.descripcion,
            id_ruta
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Ruta actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/rutas/{id_ruta}")
def delete_ruta(id_ruta: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM RUTAS WHERE id_ruta = %s;", (id_ruta,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Ruta eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Endpoints para HISTORIAL DE ACTIVIDADES -----


@app.get("/historial")
def get_historial():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM historial_actividades;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/historial/{id_historial}")
def get_historial_item(id_historial: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM historial_actividades WHERE id_historial = %s;", (id_historial,))
        historial = cur.fetchone()
        cur.close()
        conn.close()
        if historial is None:
            raise HTTPException(
                status_code=404, detail="Historial no encontrado")
        return historial
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/historial")
def create_historial(historial: HistorialActividad):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO historial_actividades (id_historial, id_usuarios, id_ruta, fecha)
            VALUES (%s, %s, %s, %s);
        """
        values = (
            historial.id_historial,
            historial.id_usuarios,
            historial.id_ruta,
            historial.fecha
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Historial de actividad creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/historial/{id_historial}")
def update_historial(id_historial: int, historial: HistorialActividad):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE historial_actividades
            SET id_usuarios = %s, id_ruta = %s, fecha = %s
            WHERE id_historial = %s;
        """
        values = (
            historial.id_usuarios,
            historial.id_ruta,
            historial.fecha,
            id_historial
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Historial no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Historial de actividad actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/historial/{id_historial}")
def delete_historial(id_historial: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM historial_actividades WHERE id_historial = %s;", (id_historial,))
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Historial no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Historial de actividad eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Endpoints para ANUNCIOS -----


@app.get("/anuncios")
def get_anuncios():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ANUNCIOS;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/anuncios/{id_anuncio}")
def get_anuncio(id_anuncio: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM ANUNCIOS WHERE id_anuncios = %s;", (id_anuncio,))
        anuncio = cur.fetchone()
        cur.close()
        conn.close()
        if anuncio is None:
            raise HTTPException(
                status_code=404, detail="Anuncio no encontrado")
        return anuncio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anuncios")
def create_anuncio(anuncio: Anuncio):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO ANUNCIOS (id_anuncios, titulo, contenido, id_suscripciones)
            VALUES (%s, %s, %s, %s);
        """
        values = (
            anuncio.id_anuncios,
            anuncio.titulo,
            anuncio.contenido,
            anuncio.id_suscripciones
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Anuncio creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/anuncios/{id_anuncio}")
def update_anuncio(id_anuncio: int, anuncio: Anuncio):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE ANUNCIOS
            SET titulo = %s, contenido = %s, id_suscripciones = %s
            WHERE id_anuncios = %s;
        """
        values = (
            anuncio.titulo,
            anuncio.contenido,
            anuncio.id_suscripciones,
            id_anuncio
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Anuncio no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Anuncio actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/anuncios/{id_anuncio}")
def delete_anuncio(id_anuncio: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM ANUNCIOS WHERE id_anuncios = %s;",
                    (id_anuncio,))
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Anuncio no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Anuncio eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Endpoints para SUSCRIPCIONES_ANUNCIOS -----


@app.get("/suscripciones_anuncios")
def get_suscripciones_anuncios():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SUSCRIPCIONES_ANUNCIOS;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suscripciones_anuncios/{id_sa}")
def get_suscripcion_anuncio(id_sa: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM SUSCRIPCIONES_ANUNCIOS WHERE id_SA = %s;", (id_sa,))
        sa = cur.fetchone()
        cur.close()
        conn.close()
        if sa is None:
            raise HTTPException(
                status_code=404, detail="Relación suscripción-anuncio no encontrada")
        return sa
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/suscripciones_anuncios")
def create_suscripcion_anuncio(sa: SuscripcionAnuncio):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO SUSCRIPCIONES_ANUNCIOS (id_SA, id_suscripciones, id_anuncios, num_veces_mostrado)
            VALUES (%s, %s, %s, %s);
        """
        values = (
            sa.id_SA,
            sa.id_suscripciones,
            sa.id_anuncios,
            sa.num_veces_mostrado
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Relación suscripción-anuncio creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/suscripciones_anuncios/{id_sa}")
def update_suscripcion_anuncio(id_sa: int, sa: SuscripcionAnuncio):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE SUSCRIPCIONES_ANUNCIOS
            SET id_suscripciones = %s, id_anuncios = %s, num_veces_mostrado = %s
            WHERE id_SA = %s;
        """
        values = (
            sa.id_suscripciones,
            sa.id_anuncios,
            sa.num_veces_mostrado,
            id_sa
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Relación suscripción-anuncio no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Relación suscripción-anuncio actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/suscripciones_anuncios/{id_sa}")
def delete_suscripcion_anuncio(id_sa: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM SUSCRIPCIONES_ANUNCIOS WHERE id_SA = %s;", (id_sa,))
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Relación suscripción-anuncio no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Relación suscripción-anuncio eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
