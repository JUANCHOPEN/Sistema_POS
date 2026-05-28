# Frontend Sistema POS conectado al backend actual

Frontend en React, Vite y Tailwind CSS conectado a las rutas que existen actualmente en el backend FastAPI.

## Rutas conectadas

POST /auth/login

GET /productos/

GET /productos/buscar?termino=

GET /productos/categorias

POST /productos/

GET /productos/alertas-stock

## Rutas aun pendientes en backend

POST /ventas

GET /ventas

GET /clientes

POST /clientes

GET /facturas

GET /reportes/dashboard

GET /reportes/ventas

## Instalacion

npm install

## Configuracion

Crear el archivo .env con:

VITE_API_URL=http://localhost:8000

## Ejecucion

npm run dev

## Pruebas

npm run test

## Build

npm run build
