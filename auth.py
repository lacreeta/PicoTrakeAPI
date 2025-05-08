from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import os

# Configuración del JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #type: ignore
    return token


def verificar_token(token: str) -> dict:
    """
    Decodifica y verifica el token JWT.
    Si el token es inválido o ha expirado, lanza una excepción HTTP.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401, detail="Token inválido o expirado")


def obtener_usuario_actual(token: str = Security(oauth2_scheme)) -> dict:
    """
    Dependencia de FastAPI que extrae el id_usuario del token JWT.
    Se espera que el token incluya el campo "sub" con el id_usuario.
    """
    payload = verificar_token(token)
    id_usuario = payload.get("sub")
    if id_usuario is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    try:
        id_usuario = int(id_usuario)  # Convertir a entero
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido: ID de usuario no es un número")
    return {"id_usuario": id_usuario}