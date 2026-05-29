from sqlalchemy.orm import Session
from models.usuario import Usuario
from repositories.usuario import UsuarioRepository
from schemas.usuario import UsuarioCreate, Token
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración
SECRET_KEY              = os.getenv("SECRET_KEY")
ALGORITHM               = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES") or 60)
MAX_INTENTOS_FALLIDOS   = 5

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Repositorio
usuario_repo = UsuarioRepository()

class AuthService:

    # Verificar contraseña
    def verificar_contrasena(self, contrasena: str, hash: str):
        return pwd_context.verify(contrasena, hash)

    # Hashear contraseña
    def hashear_contrasena(self, contrasena: str):
        return pwd_context.hash(contrasena)

    # Generar token JWT
    def generar_token(self, data: dict):
        datos = data.copy()
        expira = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        datos.update({"exp": expira})
        return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

    # Login
    def login(self, db: Session, correo: str, contrasena: str):

        # Buscar usuario
        usuario = usuario_repo.obtener_por_correo(db, correo)

        # Verificar que existe
        if not usuario:
            return None, "Usuario no encontrado"

        # Verificar que está activo
        if not usuario.activo:
            return None, "Cuenta desactivada"

        # Verificar intentos fallidos
        if usuario.intentos_fallidos >= MAX_INTENTOS_FALLIDOS:
            return None, "Cuenta bloqueada por 10 minutos"

        # Verificar contraseña
        if not self.verificar_contrasena(contrasena, usuario.contrasena_hash):
            usuario_repo.actualizar_intentos(
                db,
                usuario.id_usuario,
                usuario.intentos_fallidos + 1
            )
            restantes = MAX_INTENTOS_FALLIDOS - (usuario.intentos_fallidos + 1)
            return None, f"Contraseña incorrecta. Intentos restantes: {restantes}"

        # Login exitoso
        usuario_repo.actualizar_ultimo_acceso(db, usuario.id_usuario)

        # Generar token
        token = self.generar_token({
            "sub":      str(usuario.id_usuario),
            "correo":   usuario.correo,
            "rol":      usuario.id_rol
        })

        return token, usuario

    # Crear usuario
    def crear_usuario(self, db: Session, datos: UsuarioCreate):

        # Verificar que el correo no existe
        existente = usuario_repo.obtener_por_correo(db, datos.correo)
        if existente:
            return None, "El correo ya está registrado"

        # Crear objeto usuario
        nuevo_usuario = Usuario(
            id_rol          = datos.id_rol,
            nombre_completo = datos.nombre_completo,
            correo          = datos.correo,
            contrasena_hash = self.hashear_contrasena(datos.contrasena),
            activo          = True
        )

        return usuario_repo.crear(db, nuevo_usuario), None
