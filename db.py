from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row

def get_connection():
    try:
         """conn = psycopg.connect(
             host="localhost",
             port=5432,
             dbname="bbdd_projecte",      
             user="postgres",
             password="1234",
             row_factory=dict_row # type: ignore
         )"""
         conn = psycopg.connect(
             host="localhost",
             port=5432,
             dbname="picotrake",      
             user="andres",
             password="1234",
             row_factory=dict_row # type: ignore
         )
         return conn
    except psycopg.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {str(e)}")