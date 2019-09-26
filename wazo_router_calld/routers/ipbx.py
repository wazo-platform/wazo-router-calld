from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import ipbx as schema
from wazo_router_calld.services import ipbx as service


router = APIRouter()


@router.post("/ipbx/", response_model=schema.IPBX)
def create_ipbx(ipbx: schema.IPBXCreate, db: Session = Depends(get_db)):
    return service.create_ipbx(db=db, ipbx=ipbx)


@router.get("/ipbx/", response_model=List[schema.IPBX])
def read_ipbxs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ipbxs = service.get_ipbxs(db, skip=skip, limit=limit)
    return ipbxs


@router.get("/ipbx/{ipbx_id}", response_model=schema.IPBX)
def read_ipbx(ipbx_id: int, db: Session = Depends(get_db)):
    db_ipbx = service.get_ipbx(db, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx


@router.put("/ipbx/{ipbx_id}", response_model=schema.IPBX)
def update_carrier(
    ipbx_id: int, ipbx: schema.IPBXUpdate, db: Session = Depends(get_db)
):
    db_ipbx = service.update_ipbx(db, ipbx=ipbx, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx


@router.delete("/ipbx/{ipbx_id}", response_model=schema.IPBX)
def delete_carrier(ipbx_id: int, db: Session = Depends(get_db)):
    db_ipbx = service.delete_ipbx(db, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx
