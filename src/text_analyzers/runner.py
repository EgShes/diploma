from abc import ABC, abstractmethod
from typing import Any, Tuple

from amqp.spec import Basic
from pika.adapters.blocking_connection import BlockingChannel

from src.config import RabbitConfig, dev_logger
from src.dispatcher.schemas import Message
from src.queues.connector import RabbitConnector
from src.queues.queues_config import queues_config
from src.text_analyzers.common import Meta


class Preprocessor(ABC):
    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        pass

    @abstractmethod
    def preprocess(self, text: str):
        pass


class Analyzer(ABC):
    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        pass

    @abstractmethod
    def analyze(self, text: str):
        pass


class Postprocessor(ABC):
    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        pass

    @abstractmethod
    def postprocess(self, analyzer_output: Any):
        pass


class TextProvider(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> Tuple[str, Meta]:
        pass


class ResultPublisher(ABC):
    @abstractmethod
    def publish(self, result: Any, meta: Meta):
        pass


class Runner:
    def __init__(
        self,
        preprocessor: Preprocessor,
        analyzer: Analyzer,
        postprocessor: Postprocessor,
        result_publisher: ResultPublisher,
    ):
        self.preprocessor = preprocessor
        self.analyzer = analyzer
        self.postprocessor = postprocessor
        self.result_publisher = result_publisher

    def analyze_text(self, text: str):
        preprocessed = self.preprocessor.preprocess(text)
        analyzed = self.analyzer.analyze(preprocessed)
        postprocessed = self.postprocessor.postprocess(analyzed)
        return postprocessed

    def process(self, channel: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
        message = Message.parse_raw(body)

        for source_text in message.payload.source_texts:
            result = self.analyze_text(source_text.text)
            self.result_publisher.publish(result, Meta.parse_obj(source_text))

            dev_logger.debug(f"Successfully processed message {message}")

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self, queue: str):
        channel = RabbitConnector(RabbitConfig.url, queues_config).get_channel()
        channel.basic_consume(queue, on_message_callback=self.process)
        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
