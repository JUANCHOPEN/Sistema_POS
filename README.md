#Sistema POS con Inventario y Facturación FEL

Este proyecto corresponde a la Fase II del sistema POS. El avance actual incluye frontend funcional en React, conexión con el backend FastAPI existente, base local SQL Server y pipeline CI para validar el frontend.

Estructura principal

backend
Contiene la API en FastAPI, conexión a SQL Server, autenticación, productos, categorías y alertas de stock.

frontend/frontend1
Contiene el frontend funcional en React, Vite y Tailwind CSS.

.github/workflows/frontend-ci.yml
Contiene el pipeline de GitHub Actions para instalar dependencias, compilar y ejecutar pruebas del frontend.

Requisitos

Node.js 20 o superior

Python 3 instalado

SQL Server instalado localmente

ODBC Driver 17 for SQL Server

Git

Base de datos local

El archivo .bak original no restauró en SQL Server 2022 por incompatibilidad de versión. Para trabajar localmente se agregó el script:

backend/setup_min_db.py

Este script crea una base mínima llamada SistemaPOS con las tablas necesarias para el backend actual:

ROL

USUARIO

CATEGORIA

PRODUCTO

También inserta usuarios, roles, categorías y productos de prueba.

Crear base local

Entrar a la carpeta backend:

cd "\backend"

Crear el archivo .env del backend:

Set-Content .env @"
SECRET_KEY=pos_secret_key_dev
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=30
DATABASE_SERVER=localhost
DATABASE_NAME=SistemaPOS
"@

Ejecutar el script de base de datos:

python setup_min_db.py

Validar datos en SQL Server:

sqlcmd -S localhost -E -d SistemaPOS -Q "SELECT nombre FROM ROL; SELECT correo FROM USUARIO; SELECT codigo, nombre, stock_actual FROM PRODUCTO;"
Usuarios de prueba

Administrador

Correo:

admin@pos.gt

Contraseña:

admin123

Cajero

Correo:

cajero@pos.gt

Contraseña:

cajero123
Levantar backend

Entrar a backend:

cd "\backend"

Instalar dependencias:

python -m pip install -r requirements.txt

Levantar FastAPI:

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

Validar backend:

http://localhost:8000/health

Swagger:

http://localhost:8000/docs
Levantar frontend

Abrir otra terminal.

Entrar al frontend:

cd "\frontend\frontend1"

Crear .env del frontend:

Set-Content .env "VITE_API_URL=http://localhost:8000"

Instalar dependencias:

npm install

Levantar React:

npm run dev

Abrir:

http://localhost:5173
Funcionalidades conectadas actualmente

Login real contra el backend.

Consulta de productos desde SQL Server.

Consulta de categorías desde SQL Server.

Consulta de alertas de stock desde SQL Server.

Dashboard visual.

Pantallas de productos, inventario, punto de venta, reportes y usuarios.

Pruebas unitarias del frontend.

Build local validado.

Validaciones realizadas

Build del frontend:

npm run build

Resultado obtenido:

build ejecutado correctamente

Pruebas del frontend:

npm run test

Resultado obtenido:

4 pruebas ejecutadas
4 pruebas aprobadas
Cobertura 100 por ciento en calculos.js
Pipeline CI

El pipeline está en:

.github/workflows/frontend-ci.yml

El pipeline ejecuta:

Checkout del repositorio
Setup de Node.js 20
npm ci
npm run build
npm run test

La ruta configurada para el frontend es:

frontend/frontend1