from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import carrier as schema
from wazo_router_calld.services import carrier as service


router = APIRouter()


@router.post("/carriers/", response_model=schema.Carrier)
def create_carrier(carrier: schema.CarrierCreate, db: Session = Depends(get_db)):
    db_carrier = service.get_carrier_by_name(db, name=carrier.name)
    if db_carrier:
        raise HTTPException(status_code=400, detail="Name already registered")
    return service.create_carrier(db=db, carrier=carrier)


@router.get("/carriers/", response_model=List[schema.Carrier])
def read_carriers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carriers = service.get_carriers(db, skip=skip, limit=limit)
    return carriers


@router.get("/carriers/{carrier_id}", response_model=schema.Carrier)
def read_carrier(carrier_id: int, db: Session = Depends(get_db)):
    db_carrier = service.get_carrier(db, carrier_id=carrier_id)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier


@router.put("/carriers/{carrier_id}", response_model=schema.Carrier)
def update_carrier(
    carrier_id: int, carrier: schema.CarrierUpdate, db: Session = Depends(get_db)
):
    db_carrier = service.update_carrier(db, carrier=carrier, carrier_id=carrier_id)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier


@router.delete("/carriers/{carrier_id}", response_model=schema.Carrier)
def delete_carrier(
    carrier_id: int, db: Session = Depends(get_db)
):
    db_carrier = service.delete_carrier(db, carrier_id=carrier_id)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier
