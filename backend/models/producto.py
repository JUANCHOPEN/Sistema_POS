from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Categoria(Base):
    __tablename__ = "CATEGORIA"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre       = Column(String(100), nullable=False, unique=True)
    descripcion  = Column(String(255), nullable=True)

    # Relación con productos
    productos = relationship("Producto", back_populates="categoria")


class Producto(Base):
    __tablename__ = "PRODUCTO"

    id_producto    = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria   = Column(Integer, ForeignKey("CATEGORIA.id_categoria"), nullable=False)
    codigo         = Column(String(50), nullable=False, unique=True)
    nombre         = Column(String(200), nullable=False)
    precio_venta   = Column(Numeric(10,2), nullable=False)
    precio_costo   = Column(Numeric(10,2), nullable=False)
    stock_actual   = Column(Integer, nullable=False, default=0)
    stock_minimo   = Column(Integer, nullable=False, default=5)
    activo         = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)

    # Relación con categoria
    categoria = relationship("Categoria", back_populates="productos")