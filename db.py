from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import select

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="bbdd_projecte",      
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e.pgerror}")

def reset_identity():
    conn = psycopg2.connect(
        database="bbdd_projecte",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE usuarios RESTART IDENTITY CASCADE;")
    conn.commit()
       
