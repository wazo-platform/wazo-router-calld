from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import carrier_trunk as schema
from wazo_router_calld.services import carrier_trunk as service


router = APIRouter()


@router.post("/carrier_trunks/", response_model=schema.CarrierTrunk)
def create_carrier_trunk(carrier_trunk: schema.CarrierTrunkCreate, db: Session = Depends(get_db)):
    db_carrier_trunk = service.get_carrier_trunk_by_name(db, name=carrier_trunk.name)
    if db_carrier_trunk:
        raise HTTPException(status_code=400, detail="Name already registered")
    return service.create_carrier_trunk(db=db, carrier_trunk=carrier_trunk)


@router.get("/carrier_trunks/", response_model=List[schema.CarrierTrunk])
def read_carrier_trunkss(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carrier_trunks = service.get_carrier_trunks(db, skip=skip, limit=limit)
    return carrier_trunks


@router.get("/carrier_trunks/{carrier_trunk_id}", response_model=schema.CarrierTrunk)
def read_carrier_trunk(carrier_trunk_id: int, db: Session = Depends(get_db)):
    db_carrier_trunk = service.get_carrier_trunk(db, carrier_trunk_id=carrier_trunk_id)
    if db_carrier_trunk is None:
        raise HTTPException(status_code=404, detail="Carrier Trunk not found")
    return db_carrier_trunk


@router.put("/carrier_trunks/{carrier_trunk_id}", response_model=schema.CarrierTrunk)
def update_carrier_trunk(carrier_trunk_id: int, carrier_trunk: schema.CarrierTrunkUpdate, db: Session = Depends(get_db)):
    db_carrier_trunk = service.update_carrier_trunk(db, carrier_trunk=carrier_trunk, carrier_trunk_id=carrier_trunk_id)
    if db_carrier_trunk is None:
        raise HTTPException(status_code=404, detail="Carrier Trunk not found")
    return db_carrier_trunk
