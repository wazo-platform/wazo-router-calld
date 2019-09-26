from fastapi import FastAPI

from .consul import setup_consul
from .database import setup_database


def get_app(config: dict):
    app = FastAPI()
    if config.get('consul_uri') is not None:
        app = setup_consul(app, config)
    app = setup_database(app, config)

    return app
