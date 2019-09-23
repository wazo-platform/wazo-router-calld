from pydantic import BaseModel


class Carrier(BaseModel):
    id: int
    name: str = None
    tenant_id: int = None

    class Config:
        orm_mode = True


class CarrierCreate(BaseModel):
    name: str = None
    tenant_id: int = None


class CarrierUpdate(BaseModel):
    name: str = None
    tenant_id: int = None
