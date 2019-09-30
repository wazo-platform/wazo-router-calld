import responses

from json import dumps
from unittest.mock import MagicMock

from wazo_router_calld.const import METHOD_NAME

from .common import get_worker


@get_worker
@responses.activate
def test_store_cdr(worker=None):
    cdr_request = dict(
        from_uri="100@localhost",
        to_uri="200@localhost",
        call_id="1000",
        source_ip="10.0.0.1",
        source_port=5060,
        duration=60,
        call_start="2019-09-01T00:00:00",
        tenant_id=1,
    )
    cdr_response = cdr_request.copy().update(dict(
        id=1,
    ))
    responses.add(responses.POST, 'http://localhost:8000/cdrs', status=200, json=cdr_response)
    body = dict(
        method=METHOD_NAME.STORE_CDR.value,
        params=dict(
            cdr=cdr_request
        )
    )
    message = MagicMock()
    message.properties = {}
    worker.callback(
        body=body,
        message=message,
    )
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost:8000/cdrs'
    assert responses.calls[0].request.body == dumps(cdr_request).encode('utf-8')
