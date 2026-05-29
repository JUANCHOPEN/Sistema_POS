from sqlalchemy.orm import Session
from models.producto import Producto, Categoria
import random
import string

class CategoriaRepository:

    def obtener_todas(self, db: Session):
        return db.query(Categoria).all()

    def obtener_por_id(self, db: Session, id_categoria: int):
        return db.query(Categoria)\
                 .filter(Categoria.id_categoria == id_categoria)\
                 .first()

    def crear(self, db: Session, categoria: Categoria):
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria


class ProductoRepository:

    # Generar código único automático
    def generar_codigo(self, db: Session):
        while True:
            codigo = ''.join(random.choices(string.digits, k=6))
            existe = db.query(Producto)\
                       .filter(Producto.codigo == codigo)\
                       .first()
            if not existe:
                return codigo

    def obtener_todos(self, db: Session):
        return db.query(Producto)\
                 .filter(Producto.activo == True)\
                 .all()

    def obtener_por_id(self, db: Session, id_producto: int):
        return db.query(Producto)\
                 .filter(Producto.id_producto == id_producto)\
                 .first()

    def obtener_por_codigo(self, db: Session, codigo: str):
        return db.query(Producto)\
                 .filter(Producto.codigo == codigo)\
                 .first()

    def buscar(self, db: Session, termino: str):
        return db.query(Producto)\
                 .filter(
                     Producto.activo == True,
                     (Producto.nombre.contains(termino)) |
                     (Producto.codigo.contains(termino))
                 ).all()

    def obtener_alertas_stock(self, db: Session):
        return db.query(Producto)\
                 .filter(
                     Producto.activo == True,
                     Producto.stock_actual <= Producto.stock_minimo
                 ).all()

    def crear(self, db: Session, producto: Producto):
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def actualizar(self, db: Session, id_producto: int, datos: dict):
        db.query(Producto)\
          .filter(Producto.id_producto == id_producto)\
          .update(datos)
        db.commit()
        return self.obtener_por_id(db, id_producto)

    def eliminar(self, db: Session, id_producto: int):
        producto = self.obtener_por_id(db, id_producto)

        if not producto:
            return None

        producto.activo = False
        db.commit()
        db.refresh(producto)
        return producto