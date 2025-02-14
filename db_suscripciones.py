from fastapi import HTTPException
from db import get_connection
from models import Suscripcion


def readAll():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM suscripciones;")
            suscripciones = cur.fetchall()
        return suscripciones
    except Exception as e:
        raise Exception(f"Error de conexión: {e}")
    finally:
        if conn:
            conn.close()


def readById(id_suscripcion: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "select * from suscripciones where id_suscripciones = %s;", (id_suscripcion,))
            suscripcion = cur.fetchone()
        return suscripcion
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión{e}"}
    finally:
        if conn:
            conn.close()


def create(suscripcion: Suscripcion):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("insert into suscripciones (id_suscripciones, tipo, precio, duracion, fecha_fin_vigencia, estado_suscripcion) VALUES (%s, %s, %s, %s, %s, %s)",
                        (suscripcion.id_suscripciones, suscripcion.tipo, suscripcion.precio, suscripcion.duracion, suscripcion.fecha_fin_vigencia, suscripcion.estado_suscripcion))
        conn.commit()
        return {"message": "Suscripción creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


def update(id_sucripcion: int, suscripcion: Suscripcion):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("update suscripciones set tipo = %s, precio = %s, duracion = %s, fecha_fin_vigencia = %s, estado_suscripcion = %s WHERE id_suscripciones = %s",
                        (suscripcion.tipo, suscripcion.precio, suscripcion.duracion, suscripcion.fecha_fin_vigencia, suscripcion.estado_suscripcion, id_sucripcion))
            if cur.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Suscripción no encontrada")
        conn.commit()
        return {"message": "Suscripción actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
