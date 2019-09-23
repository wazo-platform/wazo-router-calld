from sqlalchemy.orm import Session

from wazo_router_calld.models.domain import Domain
from wazo_router_calld.schemas import domain as schema


def get_domain_by_id(db: Session, domain_id: int):
    return db.query(Domain).filter(Domain.id == domain_id).first()


def get_domain(db: Session, domain: str):
    return db.query(Domain).filter(Domain.domain == domain).first()


def get_domains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Domain).offset(skip).limit(limit).all()


def get_domains_by_tenant(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Domain)
        .filter(Domain.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_domain(db: Session, domain: schema.DomainCreate):
    db_domain = Domain(domain=domain.domain, tenant_id=domain.tenant_id)
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain


def update_domain(db: Session, domain_id: int, domain: schema.DomainUpdate):
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if db_domain is not None:
        db_domain.domain = (
            domain.domain if domain.domain is not None else db_domain.domain
        )
        db_domain.tenant_id = (
            domain.tenant_id if domain.tenant_id is not None else db_domain.tenant_id
        )
        db.commit()
        db.refresh(db_domain)
    return db_domain
