from pydantic import BaseModel
from typing import List


class DetalleVentaCreate(BaseModel):
    id_producto: int
    cantidad: int


class VentaCreate(BaseModel):
    id_usuario: int
    detalles: List[DetalleVentaCreate]


class DetalleVentaResponse(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


class VentaResponse(BaseModel):
    id_venta: int
    id_usuario: int
    total: float
    detalles: List[DetalleVentaResponse]

    class Config:
        from_attributes = True
