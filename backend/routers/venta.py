from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.venta import VentaCreate, VentaResponse
from services.venta import VentaService
from typing import List

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

venta_service = VentaService()


@router.post("/", response_model=VentaResponse)
def crear_venta(datos: VentaCreate, db: Session = Depends(get_db)):
    venta, error = venta_service.crear(db, datos)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return venta


@router.get("/", response_model=List[VentaResponse])
def obtener_ventas(db: Session = Depends(get_db)):
    return venta_service.obtener_todas(db)


@router.get("/{id_venta}", response_model=VentaResponse)
def obtener_venta(id_venta: int, db: Session = Depends(get_db)):
    venta, error = venta_service.obtener_por_id(db, id_venta)

    if error:
        raise HTTPException(status_code=404, detail=error)

    return venta
