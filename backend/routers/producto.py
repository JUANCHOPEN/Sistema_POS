from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.producto import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    CategoriaCreate, CategoriaResponse, AlertaStockResponse
)
from services.producto import ProductoService, CategoriaService
from typing import List

router = APIRouter(
    prefix="/productos",
    tags=["Productos e Inventario"]
)

producto_service  = ProductoService()
categoria_service = CategoriaService()

# ─── CATEGORIAS ───────────────────────────────

@router.get("/categorias", response_model=List[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    return categoria_service.obtener_todas(db)

@router.post("/categorias", response_model=CategoriaResponse)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    categoria, error = categoria_service.crear(db, datos)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return categoria

# ─── PRODUCTOS ────────────────────────────────

@router.get("/", response_model=List[ProductoResponse])
def obtener_productos(db: Session = Depends(get_db)):
    return producto_service.obtener_todos(db)

@router.get("/buscar", response_model=List[ProductoResponse])
def buscar_productos(termino: str, db: Session = Depends(get_db)):
    return producto_service.buscar(db, termino)

@router.get("/alertas-stock", response_model=List[AlertaStockResponse])
def alertas_stock(db: Session = Depends(get_db)):
    return producto_service.obtener_alertas_stock(db)

@router.post("/", response_model=ProductoResponse)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    producto, error = producto_service.crear(db, datos)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return producto

@router.put("/{id_producto}", response_model=ProductoResponse)
def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db)
):
    producto, error = producto_service.actualizar(db, id_producto, datos)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return producto
@router.delete("/{id_producto}")
def eliminar_producto(id_producto: int, db: Session = Depends(get_db)):
    producto, error = producto_service.eliminar(db, id_producto)

    if error:
        raise HTTPException(status_code=404, detail=error)

    return {
        "mensaje": "Producto eliminado correctamente",
        "id_producto": id_producto
    }