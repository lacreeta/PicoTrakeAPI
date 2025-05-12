from fastapi import HTTPException
from db import get_connection
from model.models import Suscripcion, SuscriptionUpdate


def readAll():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM suscripciones;")
            suscripciones = cur.fetchall()
        return suscripciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se ha encontrado ninguna suscripción.")
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
            cur.execute("insert into suscripciones (id_suscripciones, tipo, precio) VALUES (%s, %s, %s)",
                        (suscripcion.id_suscripciones, suscripcion.tipo, suscripcion.precio))
        conn.commit()
        return {"message": "Suscripción creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


def update(id_suscripcion: int, suscripcion: SuscriptionUpdate):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("update suscripciones set tipo = %s, precio = %s WHERE id_suscripciones = %s",
                        (suscripcion.tipo, suscripcion.precio, id_suscripcion))
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


def delete(id_suscripcion: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "delete from suscripciones WHERE id_suscripciones = %s", (id_suscripcion,))
            if cur.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Suscripción no encontrada")
        conn.commit()
        return {"message": "Suscripción eliminada correctamente"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error eliminando suscripción: {str(e)}")
    finally:
        if conn:
            conn.close()
