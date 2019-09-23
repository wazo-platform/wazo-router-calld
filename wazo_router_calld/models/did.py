from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class DID(Base):
    __tablename__ = "dids"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant')
    carrier_trunk_id = Column(Integer, ForeignKey('carrier_trunks.id'), nullable=False)
    carrier_trunk = relationship('Tenant')
    did_regex = Column(Text, unique=True, index=True)
