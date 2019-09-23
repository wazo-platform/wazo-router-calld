from pydantic import BaseModel


class RoutingRule(BaseModel):
    id: int
    carrier_trunk_id: int = None
    ipbx_id: int = None
    prefix: str = None
    did_regex: str = None
    route_type: str = None

    class Config:
        orm_mode = True


class RoutingRuleCreate(BaseModel):
    carrier_trunk_id: int = None
    ipbx_id: int = None
    prefix: str = None
    did_regex: str = None
    route_type: str = None


class RoutingRuleUpdate(BaseModel):
    carrier_trunk_id: int = None
    ipbx_id: int = None
    prefix: str = None
    did_regex: str = None
    route_type: str = None
