from pydantic import BaseModel


class Domain(BaseModel):
    id: int
    domain: str
    tenant_id: int

    class Config:
        orm_mode = True


class DomainCreate(BaseModel):
    domain: str
    tenant_id: int


class DomainUpdate(BaseModel):
    domain: str
    tenant_id: int
