from pydantic import BaseModel


class Domain(BaseModel):
    id: int
    domain: str = None
    tenant_id: int = None

    class Config:
        orm_mode = True


class DomainCreate(BaseModel):
    domain: str = None
    tenant_id: int = None


class DomainUpdate(BaseModel):
    domain: str = None
    tenant_id: int = None
