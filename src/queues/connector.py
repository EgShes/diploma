import socket
from typing import List

from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import (
    AMQPChannelError,
    AMQPConnectionError,
    ConnectionClosedByBroker,
)

from src.queues.queues_config import (
    BindingSchema,
    ExchangeSchema,
    QueueSchema,
    RabbitConfigSchema,
)


class ConnectionNotInitializedError(Exception):
    pass


class RabbitConnector:
    def __init__(self, rabbit_dsn: str, queues_config: RabbitConfigSchema):
        self.rabbit_dsn = rabbit_dsn
        self.queues_config = queues_config
        self.init_connection()

    def init_connection(self):
        self.connection = BlockingConnection(URLParameters(self.rabbit_dsn))

    def get_channel(self) -> BlockingChannel:
        channel = self.connection.channel()

        self.init_exchanges(channel, self.queues_config.exchanges)
        self.init_queues(channel, self.queues_config.queues)
        self.init_bindings(channel, self.queues_config.bindings)

        return channel

    def connection_ok(self) -> bool:
        connection = None
        try:
            connection = BlockingConnection(URLParameters(self.rabbit_dsn))
            return connection.is_open
        except (ConnectionClosedByBroker, AMQPChannelError, AMQPConnectionError, socket.gaierror):
            return False
        finally:
            if connection:
                connection.close()

    @staticmethod
    def init_exchanges(channel: BlockingChannel, exchanges: List[ExchangeSchema]):
        for exchange in exchanges:
            channel.exchange_declare(exchange=exchange.name, durable=exchange.durable, exchange_type=exchange.type)

    @staticmethod
    def init_queues(channel: BlockingChannel, queues: List[QueueSchema]):
        for queue in queues:
            channel.queue_declare(queue=queue.name, durable=queue.durable, arguments=queue.arguments)

    @staticmethod
    def init_bindings(channel: BlockingChannel, bindings: List[BindingSchema]):
        for binding in bindings:
            channel.queue_bind(exchange=binding.exchange, queue=binding.queue, routing_key=binding.routing_key)

    def close_connection(self):
        try:
            self.connection.close()
        except NameError:
            pass
