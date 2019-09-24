from typing import List

from sqlalchemy.orm import Session

from wazo_router_calld.models.routing_group import RoutingGroup
from wazo_router_calld.schemas import routing_group as schema


def get_routing_group(db: Session, routing_group_id: int) -> RoutingGroup:
    return db.query(RoutingGroup).filter(RoutingGroup.id == routing_group_id).first()


def get_routing_groups(
    db: Session, skip: int = 0, limit: int = 100
) -> List[RoutingGroup]:
    return db.query(RoutingGroup).offset(skip).limit(limit).all()


def create_routing_group(
    db: Session, routing_group: schema.RoutingGroupCreate
) -> RoutingGroup:
    db_routing_group = RoutingGroup(
        routing_rule=routing_group.routing_rule, tenant_id=routing_group.tenant_id
    )
    db.add(db_routing_group)
    db.commit()
    db.refresh(db_routing_group)
    return db_routing_group


def update_routing_group(
    db: Session, routing_group_id: int, routing_group: schema.RoutingGroupUpdate
) -> RoutingGroup:
    db_routing_group = (
        db.query(RoutingGroup).filter(RoutingGroup.id == routing_group_id).first()
    )
    if db_routing_group is not None:
        db_routing_group.routing_rule = (
            routing_group.routing_rule
            if routing_group.routing_rule is not None
            else db_routing_group.routing_rule
        )
        db_routing_group.tenant_id = (
            routing_group.tenant_id
            if routing_group.tenant_id is not None
            else db_routing_group.tenant_id
        )
        db.commit()
        db.refresh(db_routing_group)
    return db_routing_group


def delete_routing_group(db: Session, routing_group_id: int) -> RoutingGroup:
    db_routing_group = (
        db.query(RoutingGroup).filter(RoutingGroup.id == routing_group_id).first()
    )
    if db_routing_group is not None:
        db.delete(db_routing_group)
        db.commit()
    return db_routing_group
