from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import LoginRequest, UsuarioCreate, Token, UsuarioResponse
from services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

auth_service = AuthService()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    token, resultado = auth_service.login(db, request.correo, request.contrasena)

    if not token:
        raise HTTPException(status_code=401, detail=resultado)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": resultado
    }

@router.post("/usuarios", response_model=UsuarioResponse)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    usuario, error = auth_service.crear_usuario(db, datos)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return usuario