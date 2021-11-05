from abc import ABC, abstractmethod
from time import sleep
from typing import Any, Dict, Tuple

Meta = Dict[str, Any]


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
        text_provider: TextProvider,
        result_publisher: ResultPublisher,
    ):
        self.preprocessor = preprocessor
        self.analyzer = analyzer
        self.postprocessor = postprocessor
        self.text_provider = iter(text_provider)
        self.result_publisher = result_publisher

    def analyze_text(self, text: str):
        preprocessed = self.preprocessor.preprocess(text)
        analyzed = self.analyzer.analyze(preprocessed)
        postprocessed = self.postprocessor.postprocess(analyzed)
        return postprocessed

    def run(self):
        while True:
            try:
                text, meta = next(self.text_provider)
            except StopIteration:
                sleep(10)
                continue
            result = self.analyze_text(text)
            self.result_publisher.publish(result, meta)
