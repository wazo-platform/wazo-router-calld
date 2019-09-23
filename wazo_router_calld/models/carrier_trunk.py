from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .carrier import Carrier  # noqa


class CarrierTrunk(Base):
    __tablename__ = "carrier_trunks"

    id = Column(Integer, primary_key=True, index=True)
    carrier_id = Column(Integer, ForeignKey('carriers.id'), nullable=False)
    carrier = relationship('Carrier')
    name = Column(String, unique=True, index=True)
    sip_proxy = Column(String, nullable=False)
    registered = Column(Boolean, default=False)
    auth_username = Column(String(35), nullable=True)
    auth_password = Column(String(64), nullable=True)
    auth_ha1 = Column(String(128), nullable=True)
    realm = Column(String(64), nullable=True)
    registrar_proxy = Column(String(128), nullable=True)
    from_domain = Column(String(64), nullable=True)
    expire_seconds = Column(Integer, nullable=False, default=3600)
    retry_seconds = Column(Integer, nullable=False, default=30)
