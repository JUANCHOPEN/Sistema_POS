from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from sqlalchemy import text 

class Rol(Base):
    __tablename__ = "ROL"

    id_rol      = Column(Integer, primary_key=True, autoincrement=True)
    nombre      = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=True)

    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "USUARIO"

    id_usuario        = Column(Integer, primary_key=True, autoincrement=True)
    id_rol            = Column(Integer, ForeignKey("ROL.id_rol"), nullable=False)
    nombre_completo   = Column(String(150), nullable=False)
    correo            = Column(String(150), nullable=False, unique=True)
    contrasena_hash   = Column(String(255), nullable=False)
    activo            = Column(Boolean, nullable=False, default=True)
    fecha_creacion    = Column(DateTime, nullable=False, server_default=text('GETDATE()'))
    ultimo_acceso     = Column(DateTime, nullable=True)
    intentos_fallidos = Column(SmallInteger, nullable=False, default=0)

    # Relación con rol
    rol = relationship("Rol", back_populates="usuarios")