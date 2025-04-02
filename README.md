# Documentación para nacho

##  Endpoints de suscripciones

###  Obtener todas las suscripciones

**GET** `/suscripciones`

#### Descripción:
Devuelve una lista con todas las suscripciones registradas.

#### Respuesta exitosa (`200 OK`):
```json
[
  {
    "id_suscripciones": 1,
    "tipo": "Premium",
    "precio": 9.99
  },
  {
    "id_suscripciones": 2,
    "tipo": "Básica",
    "precio": 4.99
  }
]
```

### Obtener una suscripción por ID

**GET** `/suscripciones/{id_suscripcion}`

#### Descripción:
Devuelve los datos de una suscripción específica usando su ID.

* Parámetros: id_suscripcion (int): ID de la suscripción.

#### Respuesta exitosa (`200 OK`):
```json
{
  "id_suscripciones": 1,
  "tipo": "Premium",
  "precio": 9.99
}
```

### Crear una nueva suscripción

**POST** `/suscripciones`

#### Descripción:
Crea una nueva suscripción.

#### Body esperado:
```json
{
  "id_suscripciones": 3,
  "tipo": "Estudiante",
  "precio": 2.99
}
```

#### Respuesta exitosa (`200 OK`):
```json
{
  "message": "Suscripción creada correctamente"
}
```

### Actualizar una suscripción

**PUT** `/suscripciones/{id_suscripcion}`

#### Descripción:
Actualiza el tipo y precio de una suscripción existente.

* Parámetros: id_suscripcion (int): ID de la suscripción a actualizar.

#### Body esperado:
```json
{
    "tipo": "Estudiante",
    "precio": 2.99
}
```

#### Respuesta exitosa (`200 OK`):
```json
{
  "message": "Suscripción actualizada correctamente"
}
```

### Eliminar una suscripción

**DELETE** `/suscripciones/{id_suscripcion}`

#### Descripción:
Elimina una suscripción por su ID.
* Parámetros: id_suscripcion (int): ID de la suscripción a eliminar.

#### Respuesta exitosa (`200 OK`):
```json
{
  "message": "Suscripción eliminada correctamente"
}
```



## Endpoints de Usuarios


### Obtener todos los usuarios

**GET** `/usuarios`

#### Descripción:
Devuelve una lista de todos los usuarios registrados.

#### Respuesta (`200 OK`):
```json
[
  {
    "id_usuarios": 1,
    "nombre": "Andrés",
    "apellido": "González",
    "email": "andres@example.com"
  }
]
```

### Obtener un usuario por ID

**GET** `/usuarios/{id_usuario}`


#### Descripción:
Devuelve la información de un usuario por su ID.

* Parámetros: id_usuario (int): ID del usuario a consultar.

#### Respuesta (`200 OK`):
```json
{
  "id_usuarios": 1,
  "nombre": "Andrés",
  "apellido": "González",
  "email": "andres@example.com"
}
```

### Crear un nuevo usuario

**POST** `/usuarios`

#### Descripción:
Crea un nuevo usuario con los datos proporcionados.

#### Body esperado:
```json
{
  "nombre": "Andrés",
  "apellido": "González",
  "email": "andres@example.com",
  "contrasena": "miPassword123"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Usuario creado correctamente",
  "id_usuarios": 2
}
```

### Iniciar sesión
**POST** `/login`

#### Descripción:
Inicia sesión y devuelve un token JWT.

#### Body esperado:
```json
{
  "email": "andres@example.com",
  "contrasena": "miPassword123"
}
```
#### Respuesta(`200 OK`):
```json
{
  "access_token": "jwt_token_aquí",
  "token_type": "bearer"
}
```
### Actualizar datos del usuario (requiere login)
**PUT** `/usuarios/update`

#### Descripción:
Actualiza datos personales del usuario autenticado.

#### Body esperado:
```json
{
  "nombre": "NuevoNombre",
  "apellido": "NuevoApellido",
  "email": "nuevo@email.com"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Usuario actualizado correctamente"
}
```
### Cambiar contraseña (requiere login)
**PUT** `/usuarios/update/password`

#### Descripción:
Cambia la contraseña del usuario autenticado.

#### Body esperado:
```json
{
  "contrasena_actual": "oldPass",
  "nueva_contrasena": "newPass123"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "contrasena actualizada correctamente"
}
```

### Resetear contraseña (requiere login)
**PUT** `/usuarios/reset/password`

#### Descripción:
Permite resetear la contraseña del usuario autenticado.

### Body esperado:
```json
{
  "nueva_contrasena": "newPass123"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "contrasena actualizada correctamente"
}
```
### Actualizar suscripción del usuario (requiere login)
**PUT**  `/usuarios/update/suscription`

#### Descripción:
Actualiza la suscripción del usuario autenticado.

#### Body esperado:
```json
{
  "id_suscripcion": 2,
  "duracion": 12
}
```

**Duración válida: 1 mes o 12 meses.**

#### Respuesta (`200 OK`):
```json
{
  "message": "Suscripción actualizada correctamente"
}
```

### Eliminar cuenta de usuario (requiere login)
**DELETE** `/usuarios/`

#### Descripción:
Elimina la cuenta del usuario autenticado. Se requiere contraseña actual para confirmar.

#### Body esperado:
```json
{
  "contrasena": "miPassword123"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Usuario eliminado correctamente"
}
```

### Obtener todas las rutas
**GET** `/rutas`
#### Descripción: Devuelve una lista con todas las rutas.

#### Respuesta (`200 OK`):
```json
[
  ["Ruta del Sol", "Fácil", "Barcelona", "Bonita ruta al amanecer"],
  ["Caminito Verde", "Media", "Madrid", "Ruta entre árboles y lagos"]
]
```
### Obtener ruta por id
**GET** `/rutas/{id_ruta}`

#### Descripción: 
Devuelve una ruta por su ID.

#### Respuesta (`200 OK`):
```json
{
  "id_ruta": 1,
  "nombre_ruta": "Ruta del Sol",
  "dificultad": "Fácil",
  "ubicacion": "Barcelona",
  "descripcion": "Bonita ruta al amanecer"
}
```
### Obtener ruta por nombre de ruta
**GET** `/rutas/{nombre_ruta}`

#### Descripción: 
Devuelve una ruta por su nombre.

#### Respuesta (`200 OK`):
```json
{
  "nombre_ruta": "Ruta del Sol",
  "dificultad": "Fácil",
  "ubicacion": "Barcelona",
  "descripcion": "Bonita ruta al amanecer"
}
```
### Crea una nueva ruta
**POST** `/rutas`
#### Descripción:
Crea una nueva ruta.

#### Body esperado:
```json
{
  "nombre_ruta": "Ruta del Sol",
  "dificultad": "Fácil",
  "ubicacion": "Barcelona",
  "descripcion": "Bonita ruta al amanecer"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Ruta creada correctamente"
}
```
### Actualiza una ruta por nombre
**PUT** `/rutas/{nombre_ruta}`
#### Descripción: 
Actualiza los datos de una ruta existente por nombre.

#### Body esperado (puedes actualizar uno o varios campos):
```json
{
  "dificultad": "Difícil",
  "descripcion": "Ruta con subidas exigentes"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Ruta actualizada correctamente",
  "id_ruta": 3
}
```
### Elimina una ruta a partir del nombre
**DELETE** `/rutas/{nombre_ruta}`
#### Descripción:
Elimina una ruta por nombre (para desarrolladores o admins).

#### Respuesta (`200 OK`):
```json
{
  "message": "Ruta eliminada correctamente"
}
```
### Obtiene todas las rutas (requiere login)
**GET** `/historial/usuario/mis-actividades`
#### Descripción: 
Devuelve todo el historial de rutas del usuario autenticado.

#### Respuesta (`200 OK`):
```json
[
  [1, "Ruta del Sol", "2025-03-20"],
  [3, "Caminito Verde", "2025-03-18"]
]
```
### Obtiene el historial del usuario en una ruta (requiere login)

**GET** `/historial/usuario/{nombre_ruta}`
#### Descripción:
Devuelve el historial del usuario para una ruta específica.

* Parámetro: nombre_ruta (str): nombre exacto de la ruta.

#### Respuesta (`200 OK`):
```json
[
  [1, "Ruta del Sol", "2025-03-20"],
  [1, "Ruta del Sol", "2025-02-10"]
]
```
### Filtrar por fechas (requiere login)

**GET** `/historial/usuarios/filtrar`

#### Descripción: 
Filtra el historial del usuario por rango de fechas.

* Parámetros:
    - fecha_inicio (str): formato YYYY-MM-DD

    - fecha_final (str): formato YYYY-MM-DD

#### Respuesta (`200 OK`):
```json
[
  [3, "Caminito Verde", "2025-03-18"],
  [5, "Montaña Sagrada", "2025-03-12"]
]
```
### Crea un historial
**PUT** `/historial/`
#### Descripción: 
Crea una nueva entrada de historial para un usuario y ruta.

#### Body esperado:

```json
{
  "id_usuarios": 4,
  "id_ruta": 3,
  "fecha": "2025-04-02"
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Historial creado correctamente"
}
```
### Elimina todo el historial (requiere login)
**DELETE** `/usuario/historial`
#### Descripción: 
Elimina todo el historial del usuario autenticado.
#### Respuesta (`200 OK`):
```json
{
  "message": "Historial eliminado correctamente"
}
```
### Elimina todo el historial de una ruta (requiere login)
**DELETE** `/usuario/historial/{nombre_ruta}`
#### Descripción: 
Elimina el historial del usuario para una ruta específica.
* Parámetro:
    - nombre_ruta (str): nombre exacto de la ruta.
#### Respuesta (`200 OK`):
```json
{
  "message": "Historial de la ruta eliminado correctamente"
}
```

### Anuncios

**GET** `/anuncios`
#### Descripción: 
Devuelve los anuncios personalizados para el usuario autenticado (según si es nuevo, ex-premium, etc.).

**Los usuarios premium no reciben anuncios.**

#### Respuesta (`200 OK`):
```json
[
  {
    "id_anuncios": 1,
    "titulo": "¡Hazte Premium!",
    "contenido": "Consigue 50% de descuento en tu primer mes",
    "tipo_usuario": "nuevo",
    "fecha_inicio": "2025-04-01",
    "fecha_fin": "2025-04-15",
    "activo": true,
    "id_suscripciones": 1
  }
]
```

**GET** `/anuncios-publicos`

#### Descripción: 
Devuelve anuncios genéricos, visibles para todos (no personalizados).

#### Respuesta (`200 OK`):

```json
[
  {
    "id_anuncios": 7,
    "titulo": "Explora nuevas rutas",
    "contenido": "Descubre las mejores rutas de tu zona.",
    "tipo_usuario": "generico",
    "fecha_inicio": "2025-04-01",
    "fecha_fin": null,
    "activo": true,
    "id_suscripciones": null
  }
]
```

**POST** `/anuncios`

**⚠️ Endpoint para desarrolladores/admins**

#### Descripción: 
Crea un nuevo anuncio dirigido a un tipo de usuario específico.

#### Body esperado:
```json
{
  "titulo": "Vuelve a ser premium",
  "contenido": "Te damos un 50% por volver",
  "tipo_usuario": "ex-premium",
  "fecha_inicio": "2025-04-01",
  "fecha_fin": "2025-04-15",
  "activo": true,
  "id_suscripciones": 2
}
```
#### Respuesta (`200 OK`):
```json
{
  "message": "Anuncio creado correctamente"
}
```

**DELETE** `/anuncios/{id_anuncio}`
**⚠️ Endpoint para desarrolladores/admins**

#### Descripción: 
Elimina un anuncio por su ID.
#### Respuesta (`200 OK`):
```json
{
  "message": "Anuncio eliminado correctamente"
}
```


---

# Autenticación y Tokens JWT
Este sistema utiliza JWT (JSON Web Tokens) para autenticar a los usuarios y proteger los endpoints. Se requiere un token válido en cada petición protegida.

**POST** `/login`
#### Descripción: 
El usuario inicia sesión con su correo y contraseña. Si las credenciales son válidas, se devuelve un JWT.

#### Body esperado:
```json
{
  "correo": "usuario@ejemplo.com",
  "password": "123456"
}
```
#### Respuesta (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```
#### 🧾 Contenido del JWT
El token contiene:

```json
{
"sub": "1",  // ID del usuario
"exp": 1712131730  // Expiración (timestamp)
}
```
**El campo "sub" representa el ID del usuario.**

**"exp" indica la expiración, configurada por defecto en 60 minutos.**

#### 📥 ¿Cómo usar el token?
En cada petición protegida debes enviar el token en la cabecera Authorization:

```makefile
Authorization: Bearer <tu_token>
```
#### 🔧 Generación del Token
La función crear_token() crea un JWT con el contenido necesario y la expiración:

```python
def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Expira en 60 minutos por defecto
    ...
```

#### ✅ Verificación del Token
La función verificar_token() decodifica y valida el token JWT:
```python
def verificar_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
```

#### 👤 obtener_usuario_actual
Se usa como dependencia en los endpoints que requieren autenticación. **Extrae el id_usuario del token:**
```python
def obtener_usuario_actual(token: str = Security(oauth2_scheme)) -> dict:
    payload = verificar_token(token)
    id_usuario = int(payload.get("sub"))
    return {"id_usuario": id_usuario}
```
Se encarga de verificiar el token, y extraer el id del campo sub que está dentro del jwt.