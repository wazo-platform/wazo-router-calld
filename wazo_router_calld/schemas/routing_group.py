from typing import Optional

from pydantic import BaseModel


class RoutingGroup(BaseModel):
    id: int
    tenant_id: int
    routing_rule: Optional[int] = None

    class Config:
        orm_mode = True


class RoutingGroupCreate(BaseModel):
    tenant_id: int
    routing_rule: Optional[int] = None


class RoutingGroupUpdate(BaseModel):
    tenant_id: int
    routing_rule: Optional[int] = None
