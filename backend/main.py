#Reemplazar backend/main.py con este contenido si el navegador marca error CORS.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import verificar_conexion
from routers import auth, producto, venta

app = FastAPI(
    title="Sistema POS",
    description="API REST para Sistema de Punto de Venta con FEL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.101.10:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

verificar_conexion()

app.include_router(auth.router)
app.include_router(venta.router)
app.include_router(producto.router)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema POS funcionando correctamente"}

@app.get("/health")
def health_check():
    return {
        "estado": "ok",
        "backend": "FastAPI funcionando",
        "desarrollador": "William Vasquez",        "version": "1.0"
    }
from routers import auth, producto
