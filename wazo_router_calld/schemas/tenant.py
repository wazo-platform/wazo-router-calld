from pydantic import BaseModel


class Tenant(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str


class TenantUpdate(BaseModel):
    name: str
