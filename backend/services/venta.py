from sqlalchemy.orm import Session
from models.venta import Venta, DetalleVenta
from models.producto import Producto
from schemas.venta import VentaCreate
from repositories.venta import VentaRepository

venta_repo = VentaRepository()


class VentaService:

    def crear(self, db: Session, datos: VentaCreate):

        nueva_venta = Venta(
           id_usuario=datos.id_usuario,
           metodo_pago="Efectivo",
           subtotal=0,
           descuento=0,
           total=0,
           estado="Completada"
        )

        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)

        total_venta = 0

        for item in datos.detalles:
            producto = db.query(Producto).filter(
                Producto.id_producto == item.id_producto,
                Producto.activo == True
            ).first()

            if not producto:
                return None, "Producto no encontrado"

            if producto.stock_actual < item.cantidad:
                return None, "Stock insuficiente"

            subtotal = producto.precio_venta * item.cantidad

            detalle = DetalleVenta(
                id_venta=nueva_venta.id_venta,
                id_producto=producto.id_producto,
                cantidad=item.cantidad,
                precio_unitario=producto.precio_venta,
                subtotal=subtotal
            )

            producto.stock_actual -= item.cantidad
            total_venta += subtotal

            db.add(detalle)

        nueva_venta.subtotal = total_venta
        nueva_venta.total = total_venta

        db.commit()
        db.refresh(nueva_venta)

        return nueva_venta, None

    def obtener_todas(self, db: Session):
        return venta_repo.obtener_todas(db)

    def obtener_por_id(self, db: Session, id_venta: int):
        venta = venta_repo.obtener_por_id(db, id_venta)

        if not venta:
            return None, "Venta no encontrada"

        return venta, None
