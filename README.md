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

### Obtener todos los campos del usuario (requiere login)

**GET**  `/usuarios/get/meAll/`

#### Descripción:
Devuelve toda la información de un usuario por su ID

```json
{
  "nombre": "Andrés",
  "apellido": "González",
  "email": "andreu@gmail.com",
  "fecha_registro": "2025-05-08",
  "id_suscripciones": 1
}
```

### Obtener nombre del usuario (requiere login)
**GET**  `/usuarios/get/me`
```json
{
  "nombre": "Andrés"
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
  {
    "nombre_ruta": "Camí de Ronda de S’Agaró",
    "dificultad": "Fácil",
    "ubicacion": "S’Agaró, Costa Brava",
    "descripcion": "Ruta costera muy accesible con vistas espectaculares entre S’Agaró y la Platja de Sant Pol."
  },
  ...
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
  "nombre_ruta": "Camí de Ronda de S’Agaró",
  "dificultad": "Fácil",
  "ubicacion": "S’Agaró, Costa Brava",
  "descripcion": "Ruta costera muy accesible con vistas espectaculares entre S’Agaró y la Platja de Sant Pol.",
  "duracion": null,
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "MultiLineString",
          "coordinates": [
            [
              [lon, lat, elev], // Punto 1
              [lon, lat, elev], // Punto 2
              ...
            ]
          ]
        },
        "properties": {
          "name": "Nombre de la ruta",
          "desc": "Descripción u observaciones"
        }
      }
    ]
  }
}
```
### Obtener ruta por nombre de ruta
**GET** `/rutas/{nombre_ruta}`

#### Descripción: 
Devuelve una ruta por su nombre.

#### Respuesta (`200 OK`):
```json
```json
{
  "id_ruta": 1,
  "nombre_ruta": "Camí de Ronda de S’Agaró",
  "dificultad": "Fácil",
  "ubicacion": "S’Agaró, Costa Brava",
  "descripcion": "Ruta costera muy accesible con vistas espectaculares entre S’Agaró y la Platja de Sant Pol.",
  "duracion": null,
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "MultiLineString",
          "coordinates": [
            [
              [lon, lat, elev], // Punto 1
              [lon, lat, elev], // Punto 2
              ...
            ]
          ]
        },
        "properties": {
          "name": "Nombre de la ruta",
          "desc": "Descripción u observaciones"
        }
      }
    ]
  }
}
```
### Crea una nueva ruta
**POST** `/rutas`
#### Descripción:
Crea una nueva ruta.

#### Body esperado:
```json
{
  "nombre_ruta": "string",
  "dificultad": "string",
  "ubicacion": "string",
  "descripcion": "string",
  "geojson": {
  }
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
  "nombre_ruta": "string",
  "dificultad": "string",
  "ubicacion": "string",
  "descripcion": "string",
  "geojson": {
  }
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
  {
    "id_ruta": 2,
    "nombre_ruta": "Sant Jeroni - Montserrat",
    "fecha": "2025-05-12"
  },
  {
    "id_ruta": 11,
    "nombre_ruta": "linea",
    "fecha": "2025-05-08"
  }
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
  {
    "id_ruta": 11,
    "nombre_ruta": "linea",
    "fecha": "2025-05-08"
  }
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
  {
    "id_ruta": 2,
    "nombre_ruta": "Sant Jeroni - Montserrat",
    "fecha": "2025-05-12"
  },
  {
    "id_ruta": 11,
    "nombre_ruta": "linea",
    "fecha": "2025-05-08"
  }
]
```
### Crea un historial (requiere login)
**PUT** `/historial/`
#### Descripción: 
Crea una nueva entrada de historial para un usuario y ruta.

#### Body esperado:

```json
{
  "id_ruta": 0,
  "fecha": "2025-05-12"
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

## Endpoints de Montañas
### Obtener todas las montañas
**GET** `/mountains/`

#### Descripción
Devuelve una lista con todas las montañas registradas en el sistema.

#### Respuesta (`200 OK`):
```json
[
  {
    "id_montanya": 1,
    "nombre_montanya": "Aiguamolls de l’Empordà",
    "descripcion": "Parque natural con humedales y aves protegidas.",
    "dificultad": "Fácil",
    "acampar": false,
    "pernoctar": false,
    "especies_peligrosas": true,
    "geojson": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "MultiLineString",
            "coordinates": [
              [
                [3.051703505, 41.79115305, 3],
                [3.052206534, 41.791116704, 3.019],
                ...
              ]
            ]
          },
          "properties": {
            "name": "De s'Agaro a Sa Conca",
            "desc": "name=De s'Agaro a Sa Conca"
          }
        }
      ]
    }
  },
  {
    "id_montanya": 2,
    "nombre_montanya": "Otra Montaña",
    "descripcion": "Descripción de otra montaña.",
    "dificultad": "Difícil",
    "acampar": true,
    "pernoctar": true,
    "especies_peligrosas": false,
    "geojson": { ... }
  }
]
```

### Obtener una montaña por nombre
**GET** `/mountains/{nombre_montanya}`

#### Descripción
Devuelve los datos de una montaña específica utilizando su nombre.

* Parámetros:
  - nombre_montanya (string): Nombre de la montaña a consultar.

#### Respuesta (`200 OK`):
```json
{
  "id_montanya": 1,
  "nombre_montanya": "Aiguamolls de l’Empordà",
  "descripcion": "Parque natural con humedales y aves protegidas.",
  "dificultad": "Fácil",
  "acampar": false,
  "pernoctar": false,
  "especies_peligrosas": true,
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "MultiLineString",
          "coordinates": [
            [
              [3.051703505, 41.79115305, 3],
              [3.052206534, 41.791116704, 3.019],
              ...
            ]
          ]
        },
        "properties": {
          "name": "De s'Agaro a Sa Conca",
          "desc": "name=De s'Agaro a Sa Conca"
        }
      }
    ]
  }
}
```

### Crear una nueva montaña
**POST* `/montanyas`

#### Descripción
Inserta una nueva montaña en la base de datos.

#### Body esperado:
```json
{
  "nombre_montanya": "Aiguamolls de l’Empordà",
  "descripcion": "Parque natural con humedales y aves protegidas.",
  "dificultad": "Fácil",
  "acampar": false,
  "pernoctar": false,
  "especies_peligrosas": true,
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "MultiLineString",
          "coordinates": [
            [
              [3.051703505, 41.79115305, 3],
              [3.052206534, 41.791116704, 3.019],
              ...
            ]
          ]
        },
        "properties": {
          "name": "De s'Agaro a Sa Conca",
          "desc": "name=De s'Agaro a Sa Conca"
        }
      }
    ]
  }
}
```

#### Respuesta (`200 OK`):
```json 
{
  "status": 1,
  "message": "Montaña insertada correctamente"
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
    # Expira en 720 minutos por defecto
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