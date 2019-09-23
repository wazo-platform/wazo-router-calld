from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class IPBX(Base):
    __tablename__ = "ipbx"
    __table_args__ = (
        ForeignKeyConstraint(['tenant_id', 'domain_id'], ['domains.tenant_id', 'domains.id']),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    tenant = relationship("Tenant")
    domain_id = Column(Integer, nullable=False)
    domain = relationship("Domain")
    customer = Column(Integer, nullable=False)
    ip_fqdn = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=5060)
    registered = Column(Boolean, default=False, nullable=False)
    username = Column(String(50), nullable=True)
    sha1 = Column(String(128), nullable=True)
    sha1b = Column(String(128), nullable=True)
