from typing import List

from sqlalchemy.orm import Session

from wazo_router_calld.models.did import DID
from wazo_router_calld.schemas import did as schema


def get_did(db: Session, did_id: int) -> DID:
    return db.query(DID).filter(DID.id == did_id).first()


def get_did_by_regex(db: Session, regex: str) -> DID:
    return db.query(DID).filter(DID.did_regex == regex).first()


def get_dids(db: Session, skip: int = 0, limit: int = 100) -> List[DID]:
    return db.query(DID).offset(skip).limit(limit).all()


def get_dids_by_tenant_id(db: Session, tenant: int, skip: int = 0, limit: int = 100) -> List[DID]:
    return db.query(DID).filter(DID.tenant_id == tenant).offset(skip).limit(limit).all()


def create_did(db: Session, did: schema.DIDCreate) -> DID:
    db_did = DID(
        did_regex=did.did_regex,
        carrier_trunk_id=did.carrier_trunk_id,
        tenant_id=did.tenant_id,
    )
    db.add(db_did)
    db.commit()
    db.refresh(db_did)
    return db_did


def update_did(db: Session, did_id: int, did: schema.DIDUpdate) -> DID:
    db_did = db.query(DID).filter(DID.id == did_id).first()
    if db_did is not None:
        db_did.did_regex = (
            did.did_regex if did.did_regex is not None else db_did.did_regex
        )
        db_did.carrier_trunk_id = (
            did.carrier_trunk_id
            if did.carrier_trunk_id is not None
            else db_did.carrier_trunk_id
        )
        db_did.tenant_id = (
            did.tenant_id if did.tenant_id is not None else db_did.tenant_id
        )
        db.commit()
        db.refresh(db_did)
    return db_did


def delete_did(db: Session, did_id: int) -> DID:
    db_did = db.query(DID).filter(DID.id == did_id).first()
    if db_did is not None:
        db.delete(db_did)
        db.commit()
    return db_did
