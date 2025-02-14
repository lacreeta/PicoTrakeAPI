from pydantic import BaseModel
from typing import Optional
from datetime import date

class Suscripcion(BaseModel):
    id_suscripciones: int
    tipo: str
    precio: Optional[int] = None
    duracion: int
    fecha_fin_vigencia: Optional[date] = None
    estado_suscripcion: str

class Usuario(BaseModel):
    id_usuarios: int
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    fecha_registro: Optional[date] = None
    id_suscripciones: Optional[int] = None

class Ruta(BaseModel):
    id_ruta: int
    nombre_ruta: Optional[str] = None
    dificultad: Optional[str] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None

class HistorialActividad(BaseModel):
    id_historial: int
    id_usuarios: int
    id_ruta: int
    fecha: Optional[date] = None

class Anuncio(BaseModel):
    id_anuncios: int
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    id_suscripciones: int

class SuscripcionAnuncio(BaseModel):
    id_SA: int
    id_suscripciones: int
    id_anuncios: int
    num_veces_mostrado: int
