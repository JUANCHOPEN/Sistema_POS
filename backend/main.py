from fastapi import FastAPI
from database import verificar_conexion
from routers import auth, producto

app = FastAPI(
    title="Sistema POS",
    description="API REST para Sistema de Punto de Venta con FEL",
    version="1.0.0"
)

verificar_conexion()

# Registrar routers
app.include_router(auth.router)
app.include_router(producto.router)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema POS funcionando correctamente"}

@app.get("/health")
def health_check():
    return {"estado": "ok"}