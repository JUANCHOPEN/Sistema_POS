from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ─── CATEGORIAS ───────────────────────────────

class CategoriaCreate(BaseModel):
    nombre:      str
    descripcion: Optional[str] = None

class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre:       str
    descripcion:  Optional[str] = None

    class Config:
        from_attributes = True

# ─── PRODUCTOS ────────────────────────────────

class ProductoCreate(BaseModel):
    id_categoria: int
    codigo:       Optional[str] = None
    nombre:       str
    precio_venta: float
    precio_costo: float
    stock_actual: int
    stock_minimo: int = 5

class ProductoUpdate(BaseModel):
    nombre:       Optional[str]   = None
    precio_venta: Optional[float] = None
    precio_costo: Optional[float] = None
    stock_minimo: Optional[int]   = None
    id_categoria: Optional[int]   = None
    activo:       Optional[bool]  = None

class ProductoResponse(BaseModel):
    id_producto:   int
    id_categoria:  int
    codigo:        str
    nombre:        str
    precio_venta:  float
    precio_costo:  float
    stock_actual:  int
    stock_minimo:  int
    activo:        bool

    class Config:
        from_attributes = True

class AlertaStockResponse(BaseModel):
    id_producto:  int
    codigo:       str
    nombre:       str
    stock_actual: int
    stock_minimo: int