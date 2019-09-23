from pydantic import BaseModel


class IPBX(BaseModel):
    id: int
    tenant_id: int = None
    domain_id: int = None
    customer: int = None
    ip_fqdn: str = None
    port: int = None
    registered: bool = False
    username: str = None
    sha1: str = None
    sha1b: str = None

    class Config:
        orm_mode = True


class IPBXCreate(BaseModel):
    tenant_id: int = None
    domain_id: int = None
    customer: int = None
    ip_fqdn: str = None
    port: int = 5060
    registered: bool = False
    username: str = None
    sha1: str = None
    sha1b: str = None


class IPBXUpdate(BaseModel):
    tenant_id: int = None
    domain_id: int = None
    customer: int = None
    ip_fqdn: str = None
    port: int = 5060
    registered: bool = False
    username: str = None
    sha1: str = None
    sha1b: str = None
