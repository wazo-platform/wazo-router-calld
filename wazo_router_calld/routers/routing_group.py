from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import routing_group as schema
from wazo_router_calld.services import routing_group as service


router = APIRouter()


@router.post("/routing_groups/", response_model=schema.RoutingGroup)
def create_routing_group(
    routing_group: schema.RoutingGroupCreate, db: Session = Depends(get_db)
):
    return service.create_routing_group(db=db, routing_group=routing_group)


@router.get("/routing_groups/", response_model=List[schema.RoutingGroup])
def read_routing_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    routing_groups = service.get_routing_groups(db, skip=skip, limit=limit)
    return routing_groups


@router.get("/routing_groups/{routing_group_id}", response_model=schema.RoutingGroup)
def read_routing_group(routing_group_id: int, db: Session = Depends(get_db)):
    db_routing_group = service.get_routing_group(db, routing_group_id=routing_group_id)
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group


@router.put("/routing_groups/{routing_group_id}", response_model=schema.RoutingGroup)
def update_routing_group(
    routing_group_id: int,
    routing_group: schema.RoutingGroupUpdate,
    db: Session = Depends(get_db),
):
    db_routing_group = service.update_routing_group(
        db, routing_group=routing_group, routing_group_id=routing_group_id
    )
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group


@router.delete("/routing_groups/{routing_group_id}", response_model=schema.RoutingGroup)
def delete_routing_group(
    routing_group_id: int,
    db: Session = Depends(get_db),
):
    db_routing_group = service.delete_routing_group(
        db, routing_group_id=routing_group_id
    )
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group
