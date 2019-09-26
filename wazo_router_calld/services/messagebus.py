import logging
import socket

from queue import Queue as StandardQueue
from typing import Callable, Optional

from amqp.exceptions import AMQPError, ConnectionForced, ConnectionError  # type: ignore
from kombu import Connection, Consumer, Producer, Queue  # type: ignore


class MessageBusService(object):

    _uri: str
    _connection: Connection
    _connection_producer: Connection
    _consuming: bool = False
    _producer: Producer
    _producer_reply_to_consumer: Consumer
    _future: StandardQueue
    _logger: Optional[logging.Logger]

    def __init__(self, uri: str, logger: Optional[logging.Logger] = None):
        self._uri = uri
        self._logger = logger
        self._future = StandardQueue()
        self.connect()

    def connect(self):
        self._connection = Connection(self._uri)
        self._connection.connect()
        self._connection_producer = self._connection.clone()
        self._producer = Producer(self._connection_producer)
        #
        reply_queue = Queue(
            channel=self._producer.channel,
            name="amq.rabbitmq.reply-to",
            no_ack=True,
            durable=False,
        )
        self._producer_reply_to_consumer = self._producer.channel.Consumer(
            queues=[reply_queue],
            no_ack=True,
            auto_declare=True,
            callbacks=[self.on_reply_to_message],
            accept=["json"],
        )
        self._producer_reply_to_consumer.consume(no_ack=True)

    def disconnect(self):
        self._producer.close()
        self._connection_producer.close()
        self._connection.close()

    def start_consuming(
        self,
        callback: Callable,
        queue_name: str,
        prefetch_count: int = 1,
        no_ack: bool = False,
        expires: int = None,
        callback_ready: Callable = None,
    ):
        if self._logger is not None:
            self._logger.debug("Start consuming queue: %s" % queue_name)
        self._consuming = True
        while self._consuming:
            revived_connection = self._connection.clone()
            revived_connection.ensure_connection()
            channel = revived_connection.channel()
            channel.basic_qos(0, prefetch_count, True)
            queues = []
            queue_obj = Queue(
                channel=channel,
                name=queue_name,
                no_ack=no_ack,
                durable=False,
                expires=expires,
                queue_arguments={"x-max-priority": 255},
            )
            queue_obj.declare()
            queues.append(queue_obj)
            consumer = Consumer(
                revived_connection,
                queues,
                callbacks=[callback],
                accept=["json"],
                auto_declare=False,
                prefetch_count=prefetch_count,
            )
            consumer.revive(channel)
            consumer.consume()
            while self._consuming:
                callback_ready is not None and callback_ready()
                try:
                    revived_connection.drain_events(timeout=2)
                except socket.timeout:
                    revived_connection.heartbeat_check()
                except self._connection.connection_errors + (
                    AMQPError,
                    ConnectionForced,
                    ConnectionError,
                ):  # pragma: no cover
                    if self._logger is not None:
                        self._logger.exception("Connection error", stack_info=True)
                    break

    def start_consuming_replies(
        self, callback: Callable, prefetch_count: int = 1, no_ack: bool = False
    ):
        self._consuming = True
        while self._consuming:
            revived_connection = self._connection_producer.clone()
            revived_connection.ensure_connection()
            while self._consuming:
                try:
                    revived_connection.drain_events(timeout=2)
                except socket.timeout:
                    revived_connection.heartbeat_check()
                except self._connection.connection_errors + (
                    AMQPError,
                    ConnectionForced,
                    ConnectionError,
                ):  # pragma: no cover
                    if self._logger is not None:
                        self._logger.exception("Connection error", stack_info=True)
                    break

    def stop_consuming(self):
        if self._logger is not None:
            self._logger.debug("Stop consuming...")
        self._consuming = False

    def publish(
        self,
        body: dict,
        exchange: str = "",
        queue_name: str = "",
        priority: int = None,
        reply_to: str = None,
        expiration: int = None,
        correlation_id: str = None,
    ):
        while True:
            try:
                self._connection_producer.ensure_connection()
                self._producer.publish(
                    body=body,
                    exchange=exchange,
                    routing_key=queue_name,
                    priority=priority,
                    reply_to=str(reply_to) if reply_to is not None else None,
                    expiration=expiration if expiration is not None else None,
                    correlation_id=str(correlation_id)
                    if correlation_id is not None
                    else None,
                )
            except self._connection_producer.connection_errors + (
                AMQPError,
                ConnectionForced,
                ConnectionError,
            ):  # pragma: no cover
                self._connection_producer = self._connection.clone()
                self._producer.revive(self._connection_producer)
            else:
                break

    def on_reply_to_message(self, body, message):
        self._future.put(body)

    def publish_and_get_reply(self, *args, timeout: int = 1, **kw) -> Optional[dict]:
        kw['reply_to'] = "amq.rabbitmq.reply-to"
        self.publish(*args, **kw)
        try:
            self._producer_reply_to_consumer.connection.drain_events(timeout=timeout)
        except socket.timeout:  # pragma: no cover
            return None
        #
        return self._future.get(block=False)
