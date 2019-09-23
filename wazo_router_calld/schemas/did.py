from pydantic import BaseModel


class DID(BaseModel):
    id: int
    tenant_id: int = None
    carrier_trunk_id: int = None
    did_regex: str = None

    class Config:
        orm_mode = True


class DIDCreate(BaseModel):
    tenant_id: int = None
    carrier_trunk_id: int = None
    did_regex: str = None


class DIDUpdate(BaseModel):
    tenant_id: int = None
    carrier_trunk_id: int = None
    did_regex: str = None
