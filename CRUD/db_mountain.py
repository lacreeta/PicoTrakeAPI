from fastapi import HTTPException
from db import get_connection
from model.models import MountainsPublic

def readByName(nombre: str):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT nombre_montanya, descripcion, dificultad, acampar, pernoctar, especies_peligrosas
                FROM montanyas
                WHERE nombre_montanya = %s
            """, (nombre,))
            montanya = cur.fetchone()
            if montanya is None:
                raise HTTPException(status_code=404, detail="Montaña no encontrada")
        return montanya
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión{e}"}
    finally:
        if conn:
            conn.close()