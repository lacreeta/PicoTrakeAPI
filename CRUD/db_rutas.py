from fastapi import HTTPException
from db import get_connection
from model.models import Ruta

def readAll():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("select nombre_ruta, dificultad, ubicacion, descripcion from rutas;")
            rutas = cur.fetchall()
        return rutas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se ha encontrado ninguna ruta.")
    finally:
        if conn:
            conn.close()

def readById(id_ruta: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "select * from rutas where id_ruta = %s;", (id_ruta,))
            ruta = cur.fetchone()
        return ruta
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión{e}"}
    finally:
        if conn:
            conn.close()


def readByName(nombre: str):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM rutas where nombre_ruta =%s", (nombre,))
            ruta = cur.fetchone()
            if ruta is None:
                raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return ruta
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión{e}"}
    finally:
        if conn:
            conn.close()

def create(ruta: Ruta):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("insert into rutas (nombre_ruta, dificultad, ubicacion, descripcion) VALUES (%s, %s, %s, %s)",
                        (ruta.nombre_ruta, ruta.dificultad, ruta.ubicacion, ruta.descripcion))
        conn.commit()
        return {"message": "Ruta creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def update(nombre_ruta: str, ruta: Ruta):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id_ruta FROM rutas WHERE nombre_ruta = %s", (nombre_ruta,))
            resultado = cur.fetchone()
            if resultado is None:
                raise HTTPException(status_code=404, detail="Ruta no encontrada")
            id_ruta = resultado["id_ruta"]  # type: ignore

            data = {k: v for k, v in ruta.model_dump().items() if v is not None}
            
            if not data:
                raise HTTPException(status_code=400, detail="No hay datos para actualizar")

            query = "UPDATE rutas SET " + ", ".join(f"{k} = %s" for k in data.keys()) + " WHERE id_ruta = %s"
            valores = list(data.values()) + [id_ruta] 

            cur.execute(query, valores) # type: ignore

        conn.commit()
        return {"message": "Ruta actualizada correctamente", "id_ruta": id_ruta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if conn:
            conn.close()

def delete(nombre_ruta:str):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(""" delete from rutas where nombre_ruta = %s""",(nombre_ruta,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=400, detail=f"No se ha encontrado la ruta: {nombre_ruta}")
            conn.commit()
        return {"message": "Ruta borrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar la ruta: {e}")
    finally:
        if conn:
            conn.close()
