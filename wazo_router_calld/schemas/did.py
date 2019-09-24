from typing import Optional

from pydantic import BaseModel


class DID(BaseModel):
    id: int
    tenant_id: int
    carrier_trunk_id: int
    did_regex: Optional[str] = None

    class Config:
        orm_mode = True


class DIDCreate(BaseModel):
    tenant_id: int
    carrier_trunk_id: int
    did_regex: Optional[str] = None


class DIDUpdate(BaseModel):
    tenant_id: int
    carrier_trunk_id: int
    did_regex: Optional[str] = None
