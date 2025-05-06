from fastapi import HTTPException
from db import get_connection
from model.models import HistorialActividad
from datetime import datetime, timedelta

def getAll(id_usuario: int):
     conn = None
     try: 
          conn =  get_connection()
          with conn.cursor() as cur:
               consulta = """
        SELECT h.id_ruta, r.nombre_ruta, h.fecha
        FROM historial_actividades h
        JOIN rutas r ON h.id_ruta = r.id_ruta
        WHERE h.id_usuarios = %s
        ORDER BY h.fecha DESC;
        """
               cur.execute(consulta, (id_usuario,))
               historial = cur.fetchall()
               return historial
     except Exception as e:
          print(f"Error al obtener historial: {e}")
          return []
     finally:
          if conn:
               conn.close()

def getByRoute(id_usuario: int, nombre_ruta: str):
     conn = None
     try:
          conn = get_connection()
          with conn.cursor() as cur:
               cur.execute("""
                    SELECT h.id_ruta, r.nombre_ruta, h.fecha
                    FROM historial_actividades h 
                    JOIN rutas r ON h.id_ruta = r.id_ruta
                    WHERE h.id_usuarios = %s AND LOWER(r.nombre_ruta) LIKE LOWER(%s)
               """, (id_usuario, f"%{nombre_ruta}%"))
               historial = cur.fetchall()
               if not historial:
                    raise HTTPException(
                    status_code=404,
                    detail=f"No hay historial para la ruta '{nombre_ruta}' del usuario {id_usuario}."
                    )
               return historial
     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error al obtener el historial: {e}")
     finally:
          if conn:
               conn.close()

def getByDate(id_usuarios: int, fecha_inicio: str = "", fecha_fin: str = "", ordenar: str = "desc", page: int = 1, page_size: int = 10):
    conn = None
    try:
        if not fecha_inicio:
            fecha_inicio = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.today().strftime("%Y-%m-%d")

        orden_sql = "DESC" if ordenar.lower() == "desc" else "ASC"
        offset = (page - 1) * page_size  

        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT h.id_ruta, r.nombre_ruta, h.fecha
                FROM historial_actividades h
                JOIN rutas r ON h.id_ruta = r.id_ruta
                WHERE h.id_usuarios = %s 
                AND h.fecha BETWEEN %s AND %s
                ORDER BY h.fecha {orden_sql}
                LIMIT %s OFFSET %s;
            """, (id_usuarios, fecha_inicio, fecha_fin, page_size, offset))
            historial = cur.fetchall()
        return historial
    except Exception as e:
        raise Exception(f"Error al obtener historial: {e}")
    finally:
        if conn:
            conn.close()

def create(historial: HistorialActividad):
     try:
          conn = get_connection()
          with conn.cursor() as cur:
               cur.execute("""
                    insert into historial_actividades (id_usuarios, id_ruta, fecha)
                    values (%s, %s, %s)""", (historial.id_usuarios, historial.id_ruta, historial.fecha))
               conn.commit()
          return {"message": "Historial creado correctamente"}
     except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear historial: {e}")
     finally:
        if conn:
            conn.close()

def deleteAll(id_usuario: int):
     try:
          conn =  get_connection()
          with conn.cursor() as cur:
               cur.execute(""" delete from historial_actividades where id_usuarios = %s""", (id_usuario,))
               if cur.rowcount == 0:
                    raise HTTPException(
                    status_code=404, detail="No hay historial para borrar.")
               conn.commit()
     except Exception as e:
          raise HTTPException(status_code=400, detail=f"Error al eliminar el historial: {e}")
     finally:
          if conn:
               conn.close()

def deleteByRoute(id_usuario: int, nombre_ruta:str):
     try:
          conn = get_connection()
          with conn.cursor() as cur:
               cur.execute(""" 
                           delete from historial_actividades h 
                           join rutas r on h.id_ruta = r.id_ruta
                           where h.id_usuarios = %s and r.nombre_ruta = %s
                            """, (id_usuario, nombre_ruta))
               if cur.rowcount == 0:
                    raise HTTPException(
                    status_code=404, detail=f"No hay historial de la ruta: {nombre_ruta} para borrar.")
               conn.commit()
     except Exception as e:
          raise HTTPException(status_code=400, detail=f"Error al eliminar el historial: {e}")
     finally:
          if conn:
               conn.close()