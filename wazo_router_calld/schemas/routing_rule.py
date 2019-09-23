from typing import Optional

from pydantic import BaseModel


class RoutingRule(BaseModel):
    id: int
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[str] = None
    did_regex: Optional[str] = None
    route_type: str

    class Config:
        orm_mode = True


class RoutingRuleCreate(BaseModel):
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[str] = None
    did_regex: Optional[str] = None
    route_type: str


class RoutingRuleUpdate(BaseModel):
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[str] = None
    did_regex: Optional[str] = None
    route_type: str
