from fastapi import HTTPException
from db import get_connection
from model.models import MountainsPublic
import json

def readAll():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM montanyas")
            return cur.fetchall()
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    finally:
        if conn:
            conn.close()
            
def readByName(nombre: str):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur: 
            cur.execute("SELECT * FROM montanyas WHERE nombre_montanya = %s", (nombre,))
            montanya = cur.fetchone()
            if montanya is None:
                raise HTTPException(status_code=404, detail="Montaña no encontrada")
            return montanya
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    finally:
        if conn:
            conn.close()
            
            
def insert_montanya(data: MountainsPublic):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO montanyas 
                (nombre_montanya, descripcion, dificultad, acampar, pernoctar, especies_peligrosas, geojson)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data.nombre_montanya,
                data.descripcion,
                data.dificultad,
                data.acampar,
                data.pernoctar,
                data.especies_peligrosas,
                json.dumps(data.geojson)  
            ))
            conn.commit()
            return {"status": 1, "message": "Montaña insertada correctamente"}
    except Exception as e:
        return {"status": -1, "message": f"Error al insertar: {e}"}
    finally:
        if conn:
            conn.close()