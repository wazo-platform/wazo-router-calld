from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(64), unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant')
