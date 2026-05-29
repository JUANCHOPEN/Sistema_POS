from sqlalchemy.orm import Session
from models.producto import Producto, Categoria
from repositories.producto import ProductoRepository, CategoriaRepository
from schemas.producto import ProductoCreate, ProductoUpdate, CategoriaCreate

producto_repo  = ProductoRepository()
categoria_repo = CategoriaRepository()

class CategoriaService:

    def obtener_todas(self, db: Session):
        return categoria_repo.obtener_todas(db)

    def crear(self, db: Session, datos: CategoriaCreate):
        nueva = Categoria(
            nombre      = datos.nombre,
            descripcion = datos.descripcion
        )
        return categoria_repo.crear(db, nueva), None


class ProductoService:

    def obtener_todos(self, db: Session):
        return producto_repo.obtener_todos(db)

    def buscar(self, db: Session, termino: str):
        return producto_repo.buscar(db, termino)

    def obtener_alertas_stock(self, db: Session):
        return producto_repo.obtener_alertas_stock(db)

    def crear(self, db: Session, datos: ProductoCreate):

        # Verificar que la categoría existe
        categoria = categoria_repo.obtener_por_id(db, datos.id_categoria)
        if not categoria:
            return None, "Categoría no encontrada"

        # Generar código si no se ingresó uno
        codigo = datos.codigo
        if not codigo:
            codigo = producto_repo.generar_codigo(db)
        else:
            # Verificar que el código no existe
            existente = producto_repo.obtener_por_codigo(db, codigo)
            if existente:
                return None, "Ya existe un producto con ese código"

        nuevo = Producto(
            id_categoria = datos.id_categoria,
            codigo       = codigo,
            nombre       = datos.nombre,
            precio_venta = datos.precio_venta,
            precio_costo = datos.precio_costo,
            stock_actual = datos.stock_actual,
            stock_minimo = datos.stock_minimo
        )
        return producto_repo.crear(db, nuevo), None

    def actualizar(self, db: Session, id_producto: int, datos: ProductoUpdate):

        producto = producto_repo.obtener_por_id(db, id_producto)
        if not producto:
            return None, "Producto no encontrado"

        # Solo actualizar campos que se enviaron
        cambios = {k: v for k, v in datos.model_dump().items()
                   if v is not None}

        return producto_repo.actualizar(db, id_producto, cambios), None
              

    def eliminar(self, db: Session, id_producto: int):
        producto = producto_repo.obtener_por_id(db, id_producto)

        if not producto:
            return None, "Producto no encontrado"

        return producto_repo.eliminar(db, id_producto), None
