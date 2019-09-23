from sqlalchemy.orm import Session

from wazo_router_calld.models.ipbx import IPBX
from wazo_router_calld.schemas import ipbx as schema


def get_ipbx(db: Session, ipbx_id: int):
    return db.query(IPBX).filter(IPBX.id == ipbx_id).first()


def get_ipbx_by_ip_fqdn(db: Session, ip_fqdn: str):
    return db.query(IPBX).filter(IPBX.ip_fqdn == ip_fqdn).first()


def get_ipbxs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(IPBX).offset(skip).limit(limit).all()


def get_ipbxs_by_tenant(db: Session, tenant: int, skip: int = 0, limit: int = 100):
    return db.query(IPBX).filter(IPBX.tenant == tenant).offset(skip).limit(limit).all()


def create_ipbx(db: Session, ipbx: schema.IPBXCreate):
    db_ipbx = IPBX(
        tenant_id=ipbx.tenant_id,
        domain_id=ipbx.domain_id,
        customer=ipbx.customer,
        ip_fqdn=ipbx.ip_fqdn,
        port=ipbx.port,
        registered=ipbx.registered,
        username=ipbx.username,
        sha1=ipbx.sha1,
        sha1b=ipbx.sha1b,
    )
    db.add(db_ipbx)
    db.commit()
    db.refresh(db_ipbx)
    return db_ipbx


def update_ipbx(db: Session, ipbx_id: int, ipbx: schema.IPBXUpdate):
    db_ipbx = db.query(IPBX).filter(IPBX.id == ipbx_id).first()
    if db_ipbx is not None:
        db_ipbx.tenant_id = (
            ipbx.tenant_id if ipbx.tenant_id is not None else db_ipbx.tenant_id
        )
        db_ipbx.domain_id = (
            ipbx.domain_id if ipbx.domain_id is not None else db_ipbx.domain_id
        )
        db_ipbx.customer = (
            ipbx.customer if ipbx.customer is not None else db_ipbx.customer
        )
        db_ipbx.ip_fqdn = ipbx.ip_fqdn if ipbx.ip_fqdn is not None else db_ipbx.ip_fqdn
        db_ipbx.port = ipbx.port if ipbx.port is not None else db_ipbx.port
        db_ipbx.registered = (
            ipbx.registered if ipbx.registered is not None else db_ipbx.registered
        )
        db_ipbx.username = (
            ipbx.username if ipbx.username is not None else db_ipbx.username
        )
        db_ipbx.sha1 = ipbx.sha1 if ipbx.sha1 is not None else db_ipbx.sha1
        db_ipbx.sha1b = ipbx.sha1b if ipbx.sha1b is not None else db_ipbx.sha1b
        db.commit()
        db.refresh(db_ipbx)
    return db_ipbx
