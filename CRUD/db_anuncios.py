from fastapi import HTTPException
from db import get_connection
from model.models import Anuncio

def getAnunciosParaUsuario(id_usuario: int):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Determinar tipo de usuario
            cur.execute("""
                SELECT 
                    CASE 
                        WHEN id_suscripciones = 1 AND fecha_inicio_suscripcion = fecha_registro AND fecha_final_suscripcion IS NULL 
                            THEN 'nuevo'
                        WHEN id_suscripciones != 1 AND fecha_final_suscripcion IS NULL 
                            THEN 'premium'
                        WHEN id_suscripciones = 1 AND fecha_final_suscripcion IS NOT NULL 
                            THEN 'ex-premium'
                        ELSE 'desconocido'
                    END AS tipo_usuario
                FROM USUARIOS
                WHERE id_usuarios = %s;
            """, (id_usuario,))
            tipo_usuario = cur.fetchone()
            if not tipo_usuario: 
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            if tipo_usuario == "premium":
                return []

            # Obtener los anuncios personalizados según su tipo de usuario
            cur.execute("""
                SELECT * FROM ANUNCIOS 
                WHERE tipo_usuario = %s 
                AND (fecha_fin IS NULL OR fecha_fin >= NOW())
                AND activo = TRUE;
            """, (tipo_usuario,))
            anuncios = cur.fetchall()
            return anuncios
    except Exception as e:
        print(f"Error al obtener anuncios: {e}")
        return []
    finally:
        if conn:
            conn.close()
            
def getAnunciosGenericos():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM ANUNCIOS 
                WHERE tipo_usuario = %s 
                AND (fecha_fin IS NULL OR fecha_fin >= NOW())
                AND activo = TRUE;
            """, ("generico",)) 
            anuncios = cur.fetchall()
            return anuncios
    except Exception as e:
        print(f"Error al obtener anuncios genéricos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def create(anuncio: Anuncio):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO anuncios 
                (titulo, contenido, tipo_usuario, fecha_inicio, fecha_fin, activo, id_suscripciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                anuncio.titulo,
                anuncio.contenido,
                anuncio.tipo_usuario,
                anuncio.fecha_inicio,
                anuncio.fecha_fin,
                anuncio.activo,
                anuncio.id_suscripciones
            ))  
            if cur.rowcount == 0:
                raise HTTPException(status_code=400, detail="No se ha podido crear el anuncio.")
            conn.commit()
        return {"message": "Anuncio creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el anuncio: {e}")
    finally: 
        if conn:
            conn.close()

def delete(id_anuncio: int):
    try: 
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("delete from anuncios where id_anuncios = %s", (id_anuncio,))
            if cur.rowcount == 0:
                raise HTTPException(
                status_code=404, detail="Anuncio no encontrado")
            conn.commit()
            return {"message": "Anuncio eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally: 
        if conn:
            conn.close()