from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class Suscripcion(BaseModel):
    id_suscripciones: int
    tipo: str
    precio: Optional[float] = None


class Usuario(BaseModel):
    id_usuarios: int
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = Field(None, min_length=6) 
    fecha_registro: Optional[date] = None
    id_suscripciones: Optional[int] = None
    

class Ruta(BaseModel):
    nombre_ruta: Optional[str] = None
    dificultad: Optional[str] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None


class HistorialActividad(BaseModel):
    id_usuarios: int
    id_ruta: int
    fecha: Optional[date] = None
    



# class Anuncio(BaseModel):
#     titulo: Optional[str] = None
#     contenido: Optional[str] = None
#     tipo_usuario: Optional[str] = None  # "nuevo" o "ex-premium"
#     fecha_inicio: Optional[date] = None
#     fecha_fin: Optional[date] = None
#     activo: Optional[bool] = True
#     id_suscripciones: Optional[int] = None



# class SuscripcionAnuncio(BaseModel):
#     id_SA: int
#     id_suscripciones: int
#     id_anuncios: int
#     num_veces_mostrado: int


 # Seguridad y JWT
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    contrasena: str

class UpdatePasswordRequest(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str

class DeleteUser(BaseModel):
    contrasena: str

class UsuarioResponse(BaseModel):
    id_usuarios: int
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_registro: Optional[date] = None
    id_suscripciones: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    contrasena: str

class UpdateUserRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdateSuscriptionUserModel(BaseModel):
    id_suscripcion: int
    duracion: int = Field(..., description="Duración en meses (1 o 12)") 

class SuscriptionUpdate(BaseModel):
    tipo: str
    precio: float

# Modelo para la solicitud de reset
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
# Modelo para el reset de contraseña
class ResetPasswordRequest(BaseModel):
    nueva_contrasena: str
