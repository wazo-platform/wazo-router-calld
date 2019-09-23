from typing import Optional

from pydantic import BaseModel


class IPBX(BaseModel):
    id: int
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: str
    port: int = 5060
    registered: bool = False
    username: Optional[str] = None
    sha1: Optional[str] = None
    sha1b: Optional[str] = None

    class Config:
        orm_mode = True


class IPBXCreate(BaseModel):
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: str
    port: int = 5060
    registered: bool = False
    username: Optional[str] = None
    sha1: Optional[str] = None
    sha1b: Optional[str] = None


class IPBXUpdate(BaseModel):
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: str
    port: int = 5060
    registered: bool = False
    username: Optional[str] = None
    sha1: Optional[str] = None
    sha1b: Optional[str] = None
