from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from CRUD import db_anuncios, db_usuario, db_historial, db_suscripciones, db_rutas
from model.models import *
from model.modelsBBDD import *
from typing import List
from auth import *
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from sqlmodel import SQLModel, create_engine
import os

app = FastAPI(debug=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True) # type: ignore

# Modificar Swagger para que solo pida el token JWT al autenticarse
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de PicoTrake"}

# ----- Endpoints para SUSCRIPCIONES -----

# for developers
@app.get("/suscripciones", response_model=List[Suscripcion])
def get_suscripciones():
    suscripciones_data = db_suscripciones.readAll()
    if not suscripciones_data:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ninguna suscripción")
    return suscripciones_data

@app.get("/suscripciones/{id_suscripcion}")
def get_suscripcion(id_suscripcion: int):
    if db_suscripciones.readById(id_suscripcion) is not None:
        suscripcion = db_suscripciones.readById(id_suscripcion)
    else:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ninguna suscripción por esta ID")
    return suscripcion

# for developers
@app.post("/suscripciones")
async def create_suscripcion(suscripcion: Suscripcion):
    return db_suscripciones.create(suscripcion)

# for developers
@app.put("/suscripciones/{id_suscripcion}")
def update_suscripcion(id_suscripcion: int, suscripcion: SuscriptionUpdate):
    return db_suscripciones.update(id_suscripcion, suscripcion)

# for developers
@app.delete("/suscripciones/{id_suscripcion}")
def delete_suscripcion(id_suscripcion: int):
    return db_suscripciones.delete(id_suscripcion)

# ----- Endpoints para USUARIOS -----

# for developers
@app.get("/usuarios")
def get_usuarios():
    usuarios_data = db_usuario.readAll()
    if not usuarios_data:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ningun usuario")
    return usuarios_data

# for developers
@app.get("/usuarios/{id_usuario}")
def get_usuario(id_usuario: int):
    usuario = db_usuario.readById(id_usuario)
    if usuario is None:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado ningún usuario por esta ID"
        )
    return usuario

@app.get("/usuarios/get/me")
def get_usuario(usuario: dict = Depends(obtener_usuario_actual)): 
    id_usuario = usuario["id_usuario"]
    return db_usuario.get_user(id_usuario)
    
# useless for the moment
@app.get("/usuarios/{email:str}")
def get_usuarioByEmail(email:str):
    usuario = db_usuario.getByEmail(email)
    return usuario
    
@app.post("/usuarios")
async def create_usuario(usuario: UsuarioCreate):
    return db_usuario.create(usuario)

@app.put("/usuarios/update")
def update_usuario(
    data: UpdateUserRequest, 
    usuario:dict = Depends(obtener_usuario_actual)
    ):
    data_filtrada = data.model_dump(exclude_unset=True)
    return db_usuario.update(usuario["id_usuario"], data_filtrada)

@app.put("/usuarios/update/password")
def update_password_user(
    datos: UpdatePasswordRequest,
    usuario: dict = Depends(obtener_usuario_actual)
):
    id_usuario = usuario["id_usuario"]
    return db_usuario.update_password_db(id_usuario, datos.contrasena_actual, datos.nueva_contrasena)

@app.put("/usuarios/reset/password")
def reset_password(
    datos: ResetPasswordRequest,
    usuario: dict = Depends(obtener_usuario_actual)
):
    id_usuario = usuario["id_usuario"]
    return db_usuario.reset_password(id_usuario, datos.nueva_contrasena)

@app.post("/login")
def login_user(login_data: LoginRequest):
    return db_usuario.login(login_data)

@app.put("/usuarios/update/suscription")
def update_suscription_user(
    datos: UpdateSuscriptionUserModel,
    usuario: dict = Depends(obtener_usuario_actual)):
    return db_usuario.update_suscription(usuario["id_usuario"], datos)

@app.delete("/usuarios/")
def delete_usuario(
    datos: DeleteUser,
    usuario: dict = Depends(obtener_usuario_actual)              
    ):
    id_usuario = usuario["id_usuario"]
    return db_usuario.delete(id_usuario, datos.contrasena)
    
# ----- Endpoints para RUTAS -----

@app.get("/rutas")
def get_rutas():
    return db_rutas.readAll

@app.get("/rutas/{id_ruta:int}")
def get_ruta(id_ruta: int):
    return db_rutas.readById(id_ruta)

@app.get("/rutas/{nombre_ruta:str}")
def get_ruta_by_name(nombre_ruta:str):
    return db_rutas.readByName(nombre_ruta)

@app.post("/rutas")
def create_ruta(ruta: Ruta):
    return db_rutas.create(ruta)


@app.put("/rutas/{nombre_ruta}")
def update_ruta(nombre_ruta: str, ruta: Ruta):
    return db_rutas.update(nombre_ruta, ruta)

# endpoint para desarrolladores
@app.delete("/rutas/{nombre_ruta:str}")
def delete_ruta(nombre_ruta:str):
    return db_rutas.delete(nombre_ruta)

# ----- Endpoints para HISTORIAL DE ACTIVIDADES -----

@app.get("/historial/usuario/mis-actividades")
def get_historial(usuario: dict = Depends(obtener_usuario_actual)):
    id_usuario = usuario["id_usuario"]
    return db_historial.getAll(id_usuario)

@app.get("/historial/usuario/{nombre_ruta:str}")
def get_historial_by_route(nombre_ruta:str, usuario: dict = Depends(obtener_usuario_actual)):
    id_usuario = usuario["id_usuario"]
    return db_historial.getByRoute(id_usuario, nombre_ruta)

@app.get("/historial/usuarios/filtrar")
def get_historial_by_date(fecha_inicio: str, fecha_final: str, 
                          usuario : dict = Depends(obtener_usuario_actual)):
    id_usuario = usuario["id_usuario"]
    return db_historial.getByDate(id_usuario, fecha_inicio, fecha_final)

@app.put("/historial/")
def create_historial(historial: HistorialActividad):
    return db_historial.create(historial)

@app.delete("/usuario/historial")
def delete_historial(usuario: dict = Depends(obtener_usuario_actual)):
    id_usuario = usuario["id_usuario"]
    return db_historial.deleteAll(id_usuario)

@app.delete("/usuario/historial/{nombre_ruta:str}")
def delete_historial_by_route(nombre_ruta:str, usuario:dict = Depends(obtener_usuario_actual)):
    id_usuario = usuario["id_usuario"]
    return db_historial.deleteByRoute(id_usuario, nombre_ruta)

# ----- Endpoints para ANUNCIOS -----

# @app.get("/anuncios")
# def get_anunciosLog(usuario: dict = Depends(obtener_usuario_actual)):
#     id_usuario = usuario["id_usuario"]
#     return db_anuncios.getAnunciosParaUsuario(id_usuario)

# @app.get("/anuncios-publicos")
# def get_anunciosGen():
#     return db_anuncios.getAnunciosGenericos()

# # endpoint para desarrolladores
# @app.post("/anuncios")
# def create_anuncio(anuncio: Anuncio):
#     return db_anuncios.create(anuncio)

# # endpoint para desarrolladores
# @app.delete("/anuncios/{id_anuncio}")
# def delete_anuncio(id_anuncio: int):
#     return db_anuncios.delete(id_anuncio)