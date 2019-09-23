from typing import Optional

from pydantic import BaseModel


class CarrierTrunk(BaseModel):
    id: int
    carrier_id: int
    name: str
    sip_proxy: str
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    auth_ha1: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkCreate(BaseModel):
    carrier_id: int
    name: str
    sip_proxy: str
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    auth_ha1: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30


class CarrierTrunkUpdate(BaseModel):
    name: str
    sip_proxy: str
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    auth_ha1: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30
