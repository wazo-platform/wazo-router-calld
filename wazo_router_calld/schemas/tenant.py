from pydantic import BaseModel


class Tenant(BaseModel):
    id: int
    name: str = None

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str = None


class TenantUpdate(BaseModel):
    name: str = None
