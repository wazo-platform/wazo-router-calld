from typing import Optional

from pydantic import BaseModel


class RoutingRequest(BaseModel):
    event: Optional[str] = None
    source_ip: Optional[str] = None
    source_port: Optional[int] = None
    call_id: Optional[str] = None
    from_name: Optional[str] = None
    from_uri: Optional[str] = None
    from_tag: Optional[str] = None
    to_uri: Optional[str] = None
    to_name: Optional[str] = None
    to_tag: Optional[str] = None
