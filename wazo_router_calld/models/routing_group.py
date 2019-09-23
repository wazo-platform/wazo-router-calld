from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class RoutingGroup(Base):
    __tablename__ = "routing_groups"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant')
    routing_rule = Column(Integer, ForeignKey('routing_rules.id'), nullable=True)

