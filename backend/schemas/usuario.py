from pydantic import BaseModel, EmailStr  
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    correo: EmailStr  
    contrasena: str


class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: EmailStr  
    contrasena: str
    id_rol: int


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    correo: EmailStr  
    activo: bool
    id_rol: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse