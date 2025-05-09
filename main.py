from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from sqlmodel import SQLModel, create_engine
from typing import List
from contextlib import asynccontextmanager
import os

from CRUD import db_mountain, db_usuario, db_historial, db_suscripciones, db_rutas
from model.models import *
from model.modelsBBDD import *
from auth import *

# Configuración base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# JWT Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Crear app FastAPI
app = FastAPI(
    title="PicoTrake API",
    description="API para gestionar usuarios, rutas, historial y suscripciones.",
    version="1.0.0",
    debug=True,
    lifespan=lifespan
)

# Swagger con BearerAuth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de PicoTrake"}

# ----- SUSCRIPCIONES -----
@app.get("/suscripciones", response_model=List[Suscripcion], tags=["Suscripciones"])
def get_suscripciones():
    suscripciones_data = db_suscripciones.readAll()
    if not suscripciones_data:
        raise HTTPException(status_code=404, detail="No se ha encontrado ninguna suscripción")
    return suscripciones_data

@app.get("/suscripciones/{id_suscripcion}", tags=["Suscripciones"])
def get_suscripcion(id_suscripcion: int):
    suscripcion = db_suscripciones.readById(id_suscripcion)
    if suscripcion is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado ninguna suscripción por esta ID")
    return suscripcion

@app.post("/suscripciones", tags=["Suscripciones"])
def create_suscripcion(suscripcion: Suscripcion):
    return db_suscripciones.create(suscripcion)

@app.put("/suscripciones/{id_suscripcion}", tags=["Suscripciones"])
def update_suscripcion(id_suscripcion: int, suscripcion: SuscriptionUpdate):
    return db_suscripciones.update(id_suscripcion, suscripcion)

@app.delete("/suscripciones/{id_suscripcion}", tags=["Suscripciones"])
def delete_suscripcion(id_suscripcion: int):
    return db_suscripciones.delete(id_suscripcion)

# ----- USUARIOS -----
@app.get("/usuarios", tags=["Usuarios"])
def get_usuarios():
    usuarios_data = db_usuario.readAll()
    if not usuarios_data:
        raise HTTPException(status_code=404, detail="No se ha encontrado ningún usuario")
    return usuarios_data

@app.get("/usuarios/{id_usuario}", tags=["Usuarios"])
def get_usuario(id_usuario: int):
    usuario = db_usuario.readById(id_usuario)
    if usuario is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado ningún usuario por esta ID")
    return usuario

@app.get("/usuarios/get/me", tags=["Usuarios"])
def get_usuario_me(usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.get_user(usuario["id_usuario"])

@app.get("/usuarios/get/meAll", response_model=PerfilUsuarioResponse, tags=["Usuarios"])
def get_usuario_meAll(usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.readById(usuario["id_usuario"])

@app.get("/usuarios/{email:str}", tags=["Usuarios"])
def get_usuarioByEmail(email: str):
    return db_usuario.getByEmail(email)

@app.post("/usuarios", tags=["Usuarios"])
def create_usuario(usuario: UsuarioCreate):
    return db_usuario.create(usuario)

@app.put("/usuarios/update", tags=["Usuarios"])
def update_usuario(data: UpdateUserRequest, usuario: dict = Depends(obtener_usuario_actual)):
    data_filtrada = data.model_dump(exclude_unset=True)
    return db_usuario.update(usuario["id_usuario"], data_filtrada)

@app.put("/usuarios/update/password", tags=["Usuarios"])
def update_password_user(datos: UpdatePasswordRequest, usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.update_password_db(usuario["id_usuario"], datos.contrasena_actual, datos.nueva_contrasena)

@app.put("/usuarios/reset/password", tags=["Usuarios"])
def reset_password(datos: ResetPasswordRequest, usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.reset_password(usuario["id_usuario"], datos.nueva_contrasena)

@app.put("/usuarios/update/suscription", tags=["Usuarios"])
def update_suscription_user(datos: UpdateSuscriptionUserModel, usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.update_suscription(usuario["id_usuario"], datos)

@app.delete("/usuarios/", tags=["Usuarios"])
def delete_usuario(datos: DeleteUser, usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.delete(usuario["id_usuario"], datos.contrasena)

# Login
@app.post("/login", tags=["Usuarios"])
def login_user(login_data: LoginRequest):
    return db_usuario.login(login_data)

# ----- RUTAS -----
@app.get("/rutas", tags=["Rutas"])
def get_rutas():
    return db_rutas.readAll()

@app.get("/rutas/{id_ruta:int}", tags=["Rutas"])
def get_ruta(id_ruta: int):
    return db_rutas.readById(id_ruta)

@app.get("/rutas/nombre/{nombre_ruta:str}", tags=["Rutas"])
def get_ruta_by_name(nombre_ruta: str):
    return db_rutas.readByName(nombre_ruta)

@app.post("/rutas", tags=["Rutas"])
def create_ruta(ruta: Ruta):
    return db_rutas.create(ruta)

@app.put("/rutas/{nombre_ruta}", tags=["Rutas"])
def update_ruta(nombre_ruta: str, ruta: Ruta):
    return db_rutas.update(nombre_ruta, ruta)

@app.delete("/rutas/{nombre_ruta:str}", tags=["Rutas"])
def delete_ruta(nombre_ruta: str):
    return db_rutas.delete(nombre_ruta)

# ----- HISTORIAL -----
@app.get("/historial/usuario/mis-actividades", tags=["Historial"])
def get_historial(usuario: dict = Depends(obtener_usuario_actual)):
    return db_historial.getAll(usuario["id_usuario"])

@app.get("/historial/usuario/{nombre_ruta:str}", tags=["Historial"])
def get_historial_by_route(nombre_ruta: str, usuario: dict = Depends(obtener_usuario_actual)):
    return db_historial.getByRoute(usuario["id_usuario"], nombre_ruta)

@app.get("/historial/usuarios/filtrar", tags=["Historial"])
def get_historial_by_date(
    fecha_inicio: str,
    fecha_final: str,
    usuario: dict = Depends(obtener_usuario_actual)
):
    return db_historial.getByDate(usuario["id_usuario"], fecha_inicio, fecha_final)

@app.put("/historial/", tags=["Historial"])
def create_historial(
    historial: HistorialActividadBase,
    usuario: dict = Depends(obtener_usuario_actual)
):
    return db_historial.create(HistorialActividad(
        id_usuarios=usuario["id_usuario"],
        id_ruta=historial.id_ruta,
        fecha=historial.fecha
    ))

@app.delete("/usuario/historial", tags=["Historial"])
def delete_historial(usuario: dict = Depends(obtener_usuario_actual)):
    return db_historial.deleteAll(usuario["id_usuario"])

@app.delete("/usuario/historial/{nombre_ruta:str}", tags=["Historial"])
def delete_historial_by_route(nombre_ruta: str, usuario: dict = Depends(obtener_usuario_actual)):
    return db_historial.deleteByRoute(usuario["id_usuario"], nombre_ruta)

# ----- MONTAÑAS -----

@app.get("/mountains/", tags=["Montañas"])
def get_mountains():
    return db_mountain.readAll()

@app.get("/mountains/{nombre_montanya:str}", tags=["Montañas"])
def get_mountain_by_name(nombre_montanya: str):
    return db_mountain.readByName(nombre_montanya)

@app.post("/montanyas", tags=["Montañas"])
def create_mountain(montanya: MountainsPublic):
    return db_mountain.insert_montanya(montanya)