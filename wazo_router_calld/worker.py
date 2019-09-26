import json
import logging
import os
import signal
import sys

from .services.messagebus import MessageBusService
from .const import QUEUE_NAME


class WazoRouterCalld(object):

    _context: dict
    _messagebus: MessageBusService
    _logger: logging.Logger
    _runnning: bool

    LOGGING_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def __init__(
        self,
        context: dict = None,
        messagebus: MessageBusService = None,
        signals: bool = True,
    ):
        self._context = context or {}
        self._setup_logging(self._context)
        self._messagebus = (
            messagebus
            if messagebus is not None
            else MessageBusService(
                uri=self._context["messagebus_uri"], logger=self._logger
            )
        )
        signals and (
            signal.signal(signal.SIGINT, self._graceful_exit),
            signal.signal(signal.SIGTERM, self._graceful_exit),
        )

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
        except Exception:  # pragma: no cover
            self._logger.exception("{}".format(json.dumps(body)))
        finally:
            message.ack()
