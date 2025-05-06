from datetime import date, time
from email.policy import default
from typing import Optional
from sqlmodel import SQLModel, Field, text

# Modelo para la tabla SUSCRIPCIONES
class SuscripcionDB(SQLModel, table=True):
    __tablename__ = "suscripciones"
    id_suscripciones: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(..., max_length=20)
    precio: Optional[float] = None

# Modelo para la tabla USUARIOS
class UsuarioDB(SQLModel, table=True):
    __tablename__ = "usuarios"
    id_usuarios: Optional[int] = Field(default=None, primary_key=True)
    nombre: Optional[str] = Field(default=None, max_length=100)
    apellido: Optional[str] = Field(default=None, max_length=100)
    email: str = Field(..., max_length=150, sa_column_kwargs={"unique": True})
    contrasena: str = Field(..., max_length=150)
    fecha_registro: Optional[date] = Field(default_factory=date.today)
    id_suscripciones: int = Field(default=1, foreign_key="suscripciones.id_suscripciones", sa_column_kwargs={"server_default": text("1")})
    fecha_inicio_suscripcion: Optional[date] = Field(default_factory=date.today)
    fecha_final_suscripcion: Optional[date] = None

# Modelo para la tabla RUTAS
class RutaDB(SQLModel, table=True):
    __tablename__ = "rutas"
    id_ruta: Optional[int] = Field(default=None, primary_key=True)
    nombre_ruta: Optional[str] = Field(default=None, max_length=100)
    dificultad: Optional[str] = Field(default=None, max_length=50)
    ubicacion: Optional[str] = Field(default=None, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    duracion: Optional[time] = None

# Modelo para la tabla HISTORIAL DE ACTIVIDADES
class HistorialActividadDB(SQLModel, table=True):
    __tablename__ = "historial_actividades"
    id_historial: Optional[int] = Field(default=None, primary_key=True)
    id_usuarios: int = Field(foreign_key="usuarios.id_usuarios")
    id_ruta: int = Field(foreign_key="rutas.id_ruta")
    fecha: Optional[date] = None
    
class Mountains(SQLModel, table=True):
    __tablename__ = "montanyas"
    id_montanya: Optional[int] = Field(default=None, primary_key=True)
    nombre_montanya: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    dificultad: Optional[str] = Field(default=None, max_length=50)
    acampar: bool = Field(default=True)
    pernoctar: bool = Field(default=True)
    especies_peligrosas: bool = Field(default=True)
    