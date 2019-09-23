from urllib.parse import urlparse
from uuid import uuid4
from typing import Tuple

from consul import Consul
from fastapi import FastAPI


class ConsulService(object):
    def __init__(self, consul_uri: str):
        uri = urlparse(consul_uri)
        self._consul_uri = consul_uri
        self._consul = Consul(host=uri.hostname, port=uri.port)

    def register(
        self,
        service_id: str,
        name: str,
        address: str = None,
        port: int = None,
        tags: Tuple[str] = None,
        check: dict = None,
    ):
        self._consul.agent.service.register(
            name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags,
            check=check,
        )

    def deregister(self, service_id: str):
        self._consul.agent.service.deregister(service_id)

    def get(self, key: str) -> str:
        index, data = self._consul.kv.get(key)
        return data['Value'] if data else None

    def put(self, key: str, value: str) -> bool:
        return self._consul.kv.put(key, value)


def setup_consul(app: FastAPI, config: dict):
    app.consul = ConsulService(config['consul_uri'])

    # configuration settings from consul
    database_uri = app.consul.get('wazo-router-calld.database_uri')
    if database_uri is not None:
        config['database_uri'] = database_uri.decode('utf-8')

    # register the API HTTP service on consul
    service_id = 'wazo-router-calld-%s' % uuid4()

    @app.get('/status')
    async def health():
        return {"status": "ok"}

    @app.on_event("startup")
    def startup_event():
        app.consul.register(
            service_id,
            'wazo-router-calld',
            address=config['host'] if config['host'] != '0.0.0.0' else None,
            port=config['port'],
            tags=('wazo-router-calld', 'wazo-router', 'wazo-api', 'wazo'),
            check={
                "id": "api",
                "name": "HTTP API on port 5000",
                "http": "http://%(host)s:%(port)d/status" % config,
                "method": "GET",
                "interval": "10s",
                "timeout": "1s",
            }
            if (config['host'] and config['port'])
            else None,
        )

    @app.on_event("shutdown")
    def shutdown_event():
        app.consul.deregister(service_id)

    return app
