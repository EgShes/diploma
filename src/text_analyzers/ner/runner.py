from dataclasses import dataclass
from pathlib import Path

from navec import Navec
from slovnet import NER
from slovnet.markup import SpanMarkup

from src.text_analyzers.common import RawTextProvider
from src.text_analyzers.ner.schemas import NamedEntity, NerOutputSchema
from src.text_analyzers.runner import (
    Preprocessor,
    Analyzer,
    Postprocessor,
    ResultPublisher,
    Runner,
    Meta,
)


class NerPreprocessor(Preprocessor):
    @classmethod
    def load(cls):
        return cls()

    def preprocess(self, text: str) -> str:
        return text


class NerAnalyzer(Analyzer):
    def __init__(self, model: NER):
        self._model = model

    @classmethod
    def load(cls, navec_embeddings_path: Path, ner_model_path: Path):
        navec = Navec.load(navec_embeddings_path)
        model = NER.load(ner_model_path)
        model.navec(navec)
        return cls(model)

    def analyze(self, text: str) -> SpanMarkup:
        return self._model(text)


class NerPostprocessor(Postprocessor):
    @classmethod
    def load(cls):
        return cls()

    def postprocess(self, analyzer_output: SpanMarkup) -> NerOutputSchema:
        entities = []
        for span in analyzer_output.spans:
            entities.append(
                NamedEntity(
                    text=analyzer_output.text[span.start : span.stop], type=span.type
                )
            )
        return NerOutputSchema(entities=entities)


class NerTextProvider(RawTextProvider):
    pass


class NerResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: str, meta: Meta):
        pass


if __name__ == "__main__":
    preprocessor = NerPreprocessor()
    analyzer = NerAnalyzer.load(
        Path("weights/navec_news_v1_1B_250K_300d_100q.tar"),
        Path("weights/slovnet_ner_news_v1.tar"),
    )
    postprocessor = NerPostprocessor()
    text_provider = NerTextProvider(url="http://0.0.0.0:8080/text")
    result_publisher = NerResultPublisher(url="http://0.0.0.0:8080/ner")

    ner_runner = Runner(
        preprocessor, analyzer, postprocessor, text_provider, result_publisher
    )

    ner_runner.run()
