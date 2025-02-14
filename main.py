# main.py
from fastapi import FastAPI, HTTPException
import db_suscripciones
from models import Suscripcion, Usuario, Ruta, HistorialActividad, Anuncio, SuscripcionAnuncio
from db import get_connection
from typing import List

app = FastAPI()


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
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE SUSCRIPCIONES
            SET tipo = %s, precio = %s, duracion = %s, fecha_fin_vigencia = %s, estado_suscripcion = %s
            WHERE id_suscripciones = %s;
        """
        values = (
            suscripcion.tipo,
            suscripcion.precio,
            suscripcion.duracion,
            suscripcion.fecha_fin_vigencia,
            suscripcion.estado_suscripcion,
            id_suscripcion
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Suscripción no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Suscripción actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/suscripciones/{id_suscripcion}")
def delete_suscripcion(id_suscripcion: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM SUSCRIPCIONES WHERE id_suscripciones = %s;", (id_suscripcion,))
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Suscripción no encontrada")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Suscripción eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Endpoints para USUARIOS -----


@app.get("/usuarios")
def get_usuarios():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM USUARIOS;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/usuarios/{id_usuario}")
def get_usuario(id_usuario: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM USUARIOS WHERE id_usuarios = %s;", (id_usuario,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        if usuario is None:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/usuarios")
def create_usuario(usuario: Usuario):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO USUARIOS (id_usuarios, nombre, apellido, email, contraseña, fecha_registro, id_suscripciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            usuario.id_usuarios,
            usuario.nombre,
            usuario.apellido,
            usuario.email,
            usuario.contraseña,
            usuario.fecha_registro,
            usuario.id_suscripciones
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/usuarios/{id_usuario}")
def update_usuario(id_usuario: int, usuario: Usuario):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            UPDATE USUARIOS
            SET nombre = %s, apellido = %s, email = %s, contraseña = %s, fecha_registro = %s, id_suscripciones = %s
            WHERE id_usuarios = %s;
        """
        values = (
            usuario.nombre,
            usuario.apellido,
            usuario.email,
            usuario.contraseña,
            usuario.fecha_registro,
            usuario.id_suscripciones,
            id_usuario
        )
        cur.execute(sql, values)
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Usuario actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/usuarios/{id_usuario}")
def delete_usuario(id_usuario: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM USUARIOS WHERE id_usuarios = %s;",
                    (id_usuario,))
        if cur.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
