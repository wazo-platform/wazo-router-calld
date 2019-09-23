from pydantic import BaseModel


class CarrierTrunk(BaseModel):
    id: int
    carrier_id: int = None
    name: str = None
    sip_proxy: str = None
    registered: bool = False
    auth_username: str = None
    auth_password: str = None
    auth_ha1: str = None
    realm: str = None
    registrar_proxy: str = None
    from_domain: str = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkCreate(BaseModel):
    carrier_id: int = None
    name: str = None
    sip_proxy: str = None
    registered: bool = False
    auth_username: str = None
    auth_password: str = None
    auth_ha1: str = None
    realm: str = None
    registrar_proxy: str = None
    from_domain: str = None
    expire_seconds: int = 3600
    retry_seconds: int = 30


class CarrierTrunkUpdate(BaseModel):
    name: str = None
    sip_proxy: str = None
    registered: bool = False
    auth_username: str = None
    auth_password: str = None
    auth_ha1: str = None
    realm: str = None
    registrar_proxy: str = None
    from_domain: str = None
    expire_seconds: int = 3600
    retry_seconds: int = 30
