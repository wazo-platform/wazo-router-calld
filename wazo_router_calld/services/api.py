from json import loads
from typing import Optional

import logging
import requests


class APIService(object):
    _uri: str
    _logger: Optional[logging.Logger]

    def __init__(self, uri: str, logger: Optional[logging.Logger] = None):
        self._uri = uri
        self._logger = logger

    def _call(self, method: str, uri: str, json: dict) -> Optional[dict]:
        method = method.lower()
        if method not in ('get', 'post', 'put', 'delete'):
            raise NameError('Method not found: %s' % method)
        func = getattr(requests, method)
        try:
            r = func(url="%s%s" % (self._uri, uri), json=json)
            if r.status_code == 200:
                return loads(r.content)
        except requests.exceptions.RequestException:
            pass

    def post_cdr(self, cdr: dict) -> Optional[dict]:
        return self._call('POST', '/cdrs', cdr)
