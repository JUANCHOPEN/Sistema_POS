from sqlalchemy.orm import Session
from models.venta import Venta, DetalleVenta


class VentaRepository:

    def crear_venta(self, db: Session, venta: Venta):
        db.add(venta)
        db.commit()
        db.refresh(venta)
        return venta

    def crear_detalle(self, db: Session, detalle: DetalleVenta):
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        return detalle

    def obtener_todas(self, db: Session):
        return db.query(Venta).all()

    def obtener_por_id(self, db: Session, id_venta: int):
        return db.query(Venta)\
                 .filter(Venta.id_venta == id_venta)\
                 .first()
