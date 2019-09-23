from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from wazo_router_calld.database import get_db
from wazo_router_calld.schemas import kamailio as schema
from wazo_router_calld.services import kamailio as service


router = APIRouter()


@router.post("/kamailio/routing")
def kamailio(request: schema.RoutingRequest, db: Session = Depends(get_db)):
    response = service.routing(db, request=request)
    return response
