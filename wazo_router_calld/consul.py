from typing import Optional

from urllib.parse import urlparse
from typing import Tuple

from consul import Consul  # type: ignore


class ConsulService(object):
    def __init__(self, consul_uri: str):
        uri = urlparse(consul_uri)
        self._consul_uri = consul_uri
        self._consul = Consul(host=uri.hostname, port=uri.port)

    def register(
        self,
        service_id: str,
        name: str,
        address: Optional[str] = None,
        port: Optional[int] = None,
        tags: Tuple[str] = None,
        check: Optional[dict] = None,
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

    def get(self, key: str) -> Optional[str]:
        index, data = self._consul.kv.get(key)
        return data['Value'] if data else None

    def put(self, key: str, value: str) -> bool:
        return self._consul.kv.put(key, value)


def setup_consul(config: dict):
    consul = ConsulService(config['consul_uri'])
    # configuration settings from consul
    for k in ('api_uri', 'messagebus_uri'):
        conf_value = consul.get('wazo-router-calld.%s' % k)
        if conf_value is not None:
            config[k] = conf_value

    return config
