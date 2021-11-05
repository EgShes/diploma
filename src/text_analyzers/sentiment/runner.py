from pathlib import Path
from typing import List, Dict, Any, Union

from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer

from src.text_analyzers.common import RawTextProvider
from src.text_analyzers.runner import (
    Preprocessor,
    Analyzer,
    Postprocessor,
    ResultPublisher,
    Meta,
    Runner,
)
from src.text_analyzers.sentiment.schemas import Sentiment


class SentimentPreprocessor(Preprocessor):
    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def preprocess(self, text: str) -> str:
        return text


class SentimentAnalyzer(Analyzer):
    def __init__(self, model: FastTextSocialNetworkModel):
        self._model = model

    @classmethod
    def load(cls, model_path: Union[str, Path]):
        tokenizer = RegexTokenizer()
        FastTextSocialNetworkModel.MODEL_PATH = str(model_path)
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        return cls(model)

    def analyze(self, text: str) -> List[Dict[str, float]]:
        return self._model.predict([text], k=1)


class SentimentPostprocessor(Postprocessor):
    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def postprocess(self, analyzer_output: List[Dict[str, float]]) -> Sentiment:
        sentiment_type, probability = [
            (key, value) for key, value in analyzer_output[0].items()
        ][0]
        return Sentiment(probability=probability, type=sentiment_type)


class SentimentTextProvider(RawTextProvider):
    pass


class SentimentResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: str, meta: Meta):
        pass


if __name__ == "__main__":

    preprocessor = SentimentPreprocessor()
    analyzer = SentimentAnalyzer.load(Path("/tmp/fasttext-social-network-model.bin"))
    postprocessor = SentimentPostprocessor()
    text_provider = SentimentTextProvider(url="http://0.0.0.0:8080/text")
    result_publisher = SentimentResultPublisher(url="http://0.0.0.0:8080/ner")

    runner = Runner(
        preprocessor, analyzer, postprocessor, text_provider, result_publisher
    )

    runner.run()
