from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

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