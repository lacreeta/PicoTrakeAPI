from datetime import date, time
from typing import Optional
from sqlmodel import SQLModel, Field

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
    id_suscripciones: int = Field(default=1, foreign_key="suscripciones.id_suscripciones")
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

# Modelo para la tabla ANUNCIOS
class AnuncioDB(SQLModel, table=True):
    __tablename__ = "anuncios"
    id_anuncios: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(..., max_length=100)
    contenido: str = Field(..., max_length=255)
    tipo_usuario: str = Field(..., max_length=20)  # Se espera 'nuevo' o 'ex-premium'
    fecha_inicio: Optional[date] = Field(default_factory=date.today)
    fecha_fin: Optional[date] = None
    activo: bool = Field(default=True)
    id_suscripciones: Optional[int] = Field(default=None, foreign_key="suscripciones.id_suscripciones")