from typing import Optional

from pydantic import BaseModel


class Carrier(BaseModel):
    id: int
    name: str
    tenant_id: int

    class Config:
        orm_mode = True


class CarrierCreate(BaseModel):
    name: str
    tenant_id: int


class CarrierUpdate(BaseModel):
    name: Optional[str] = None
    tenant_id: int
