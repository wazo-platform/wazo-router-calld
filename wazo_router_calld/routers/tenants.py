from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import tenant as schema
from wazo_router_calld.services import tenant as service


router = APIRouter()


@router.post("/tenants/", response_model=schema.Tenant)
def create_tenant(tenant: schema.TenantCreate, db: Session = Depends(get_db)):
    db_tenant = service.get_tenant_by_name(db, name=tenant.name)
    if db_tenant:
        raise HTTPException(status_code=400, detail="Name already registered")
    return service.create_tenant(db=db, tenant=tenant)


@router.get("/tenants/", response_model=List[schema.Tenant])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tenants = service.get_tenants(db, skip=skip, limit=limit)
    return tenants


@router.get("/tenants/{tenant_id}", response_model=schema.Tenant)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = service.get_tenant(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant


@router.put("/tenants/{tenant_id}", response_model=schema.Tenant)
def update_tenant(
    tenant_id: int, tenant: schema.TenantUpdate, db: Session = Depends(get_db)
):
    db_tenant = service.update_tenant(db, tenant_id=tenant_id, tenant=tenant)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant
