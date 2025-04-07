from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row
import os

def get_connection():
    try:
         conn = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")), #type: ignore
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            row_factory=dict_row
        )
         return conn
    except psycopg.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {str(e)}")