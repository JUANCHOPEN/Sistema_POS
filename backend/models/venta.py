from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Venta(Base):
    __tablename__ = "VENTA"

    id_venta = Column(Integer, primary_key=True, index=True)

    id_usuario = Column(Integer, ForeignKey("USUARIO.id_usuario"))

    fecha_hora = Column(DateTime, default=datetime.utcnow)

    metodo_pago = Column(String(30), default="Efectivo")
    subtotal = Column(Float, default=0)
    descuento = Column(Float, default=0)
    total = Column(Float, default=0)
    estado = Column(String(20), default="Completada")

    detalles = relationship("DetalleVenta", back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = "DETALLE_VENTA"

    id_detalle = Column(Integer, primary_key=True, index=True)

    id_venta = Column(Integer, ForeignKey("VENTA.id_venta"))

    id_producto = Column(Integer, ForeignKey("PRODUCTO.id_producto"))

    cantidad = Column(Integer)

    precio_unitario = Column(Float)

    subtotal = Column(Float)

    venta = relationship("Venta", back_populates="detalles")

