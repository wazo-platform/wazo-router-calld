from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class RoutingRule(Base):
    __tablename__ = "routing_rules"

    id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String(15), nullable=True)
    carrier_trunk_id = Column(Integer, ForeignKey('carrier_trunks.id'), nullable=False)
    carrier_trunk = relationship('CarrierTrunk')
    ipbx_id = Column(Integer, ForeignKey('ipbx.id'), nullable=False)
    ipbx = relationship('IPBX')
    did_regex = Column(Text, nullable=True)
    route_type = Column(String(10), nullable=False, default='pstn')
