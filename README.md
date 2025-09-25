# CRUD básico de usuarios en Python 3 con FasAPI, Prisma y SQLite

1. Clonar el proyecto y descargarlo en tu equipo.
2. Crear un entorno virtual en Python:
   ```
   python -m venv .venv
   ```
3. Activar el entorno virtual:
   ```
   source .venv/bin/activate
   ```
4. Instalar paquetes:
   ```
   pip install -r requirements.txt
   ```
5. Copiar .env.template y rellenar los valores de las variables de entorno:
   ´´´
   SECRET_KEY = 
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 
   ´´´
6. Ejecutar prisma para crear la base de datos:
   ```
   prisma db push
   ```
7. Ejecutar el proyecto:
   ```
   uvicorn main:app --reload
   ````

## Documentación swagger:

[localhost:8000/docs](http://localhost:8000/docs)

## Usuarios para pruebas:

- Admin:
  - username: admin@mail.com
  - password: A123456b
- User:
  - username: user@mail.com
  - password: A123456b
