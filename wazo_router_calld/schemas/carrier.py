from typing import Optional

from pydantic import BaseModel, NoneStr


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
    name: NoneStr = None
    tenant_id: Optional[int] = None
