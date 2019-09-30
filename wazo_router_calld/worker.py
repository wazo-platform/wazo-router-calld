import json
import logging
import os
import signal
import sys

from typing import Optional

from .services.api import APIService
from .services.messagebus import MessageBusService
from .const import QUEUE_NAME, METHOD_NAME


class WazoRouterCalld(object):

    _context: dict
    _messagebus: MessageBusService
    _logger: logging.Logger
    _runnning: bool

    LOGGING_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def __init__(
        self,
        context: Optional[dict] = None,
        messagebus: Optional[MessageBusService] = None,
        signals: bool = True,
    ):
        self._context = context or {}
        self._setup_logging(self._context)
        self._api = APIService(uri=self._context['api_uri'], logger=self._logger)
        self._messagebus = (
            messagebus
            if messagebus is not None
            else MessageBusService(
                uri=self._context["messagebus_uri"], logger=self._logger
            )
        )
        if signals:
            signal.signal(signal.SIGINT, self._graceful_exit)
            signal.signal(signal.SIGTERM, self._graceful_exit)

    def _graceful_exit(self, signum=None, frame=None):  # pragma: no cover
        self.stop()

    def _setup_logging(self, context: dict):
        logger = logging.getLogger("%s[%s]" % (self.__class__.__name__, os.getpid()))
        logger.setLevel(logging.DEBUG if context.get("debug") else logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG if context.get("debug") else logging.INFO)
        formatter = logging.Formatter(self.LOGGING_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self._logger = logger

    def run(self):
        self._messagebus.start_consuming(callback=self.callback, queue_name=QUEUE_NAME)

    def stop(self):
        self._messagebus.stop_consuming()

    def callback(self, body, message):
        try:
            self._logger.debug("{}".format(json.dumps(body)))
            method_name = body.get("method")
            method = {METHOD_NAME.STORE_CDR.value: self._store_cdr}.get(method_name)
            if method is not None:
                method(
                    params=body.get("params") or {},
                    correlation_id=message.properties.get("correlation_id"),
                    reply_to=message.properties.get("reply_to"),
                )
        except Exception:  # pragma: no cover
            self._logger.exception("{}".format(json.dumps(body)))
        finally:
            message.ack()

    def _store_cdr(self, params: dict, correlation_id: str, reply_to: str):
        self._api.post_cdr(params['cdr'])
