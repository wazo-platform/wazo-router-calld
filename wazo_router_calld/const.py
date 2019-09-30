from enum import Enum

QUEUE_NAME: str = "wazo_router_calld"


class METHOD_NAME(Enum):
    STORE_CDR: str = "store_cdr"
