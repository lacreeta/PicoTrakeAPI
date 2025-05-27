from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row
import os

def get_connection():
    try:
        conn = psycopg.connect(
            os.getenv("DATABASE_URL_PSYCOG"),
            row_factory=dict_row
        )
        return conn
    except psycopg.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {str(e)}")