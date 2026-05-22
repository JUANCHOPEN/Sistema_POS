from sqlalchemy.orm import Session
from models.usuario import Usuario
from datetime import datetime

class UsuarioRepository:

    # Buscar usuario por correo
    def obtener_por_correo(self, db: Session, correo: str):
        return db.query(Usuario)\
                 .filter(Usuario.correo == correo)\
                 .first()

    # Buscar usuario por ID
    def obtener_por_id(self, db: Session, id_usuario: int):
        return db.query(Usuario)\
                 .filter(Usuario.id_usuario == id_usuario)\
                 .first()

    # Obtener todos los usuarios
    def obtener_todos(self, db: Session):
        return db.query(Usuario).all()

    # Crear nuevo usuario
    def crear(self, db: Session, usuario: Usuario):
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    # Actualizar intentos fallidos
    def actualizar_intentos(self, db: Session, id_usuario: int, intentos: int):
        db.query(Usuario)\
          .filter(Usuario.id_usuario == id_usuario)\
          .update({"intentos_fallidos": intentos})
        db.commit()

    # Actualizar ultimo acceso
    def actualizar_ultimo_acceso(self, db: Session, id_usuario: int):
        db.query(Usuario)\
          .filter(Usuario.id_usuario == id_usuario)\
          .update({"ultimo_acceso": datetime.now(),
                   "intentos_fallidos": 0})
        db.commit()

    # Desactivar usuario
    def desactivar(self, db: Session, id_usuario: int):
        db.query(Usuario)\
          .filter(Usuario.id_usuario == id_usuario)\
          .update({"activo": False})
        db.commit()