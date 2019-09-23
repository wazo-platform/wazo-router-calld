from pydantic import BaseModel


class RoutingRequest(BaseModel):
    event: str = None
    source_ip: str = None
    source_port: int = None
    call_id: str = None
    from_name: str = None
    from_uri: str = None
    from_tag: str = None
    to_uri: str = None
    to_name: str = None
    to_tag: str = None
