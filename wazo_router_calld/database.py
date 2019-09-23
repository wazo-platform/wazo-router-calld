from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wazo_router_calld.models.base import Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_db(request: Request):
    return request.state.db


def setup_database(app: FastAPI, config: dict):
    database_uri = config['database_uri']
    connect_args = (
        {"check_same_thread": False} if database_uri.startswith('sqlite:') else {}
    )
    app.engine = engine = create_engine(database_uri, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = SessionLocal(bind=engine)
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    return app
