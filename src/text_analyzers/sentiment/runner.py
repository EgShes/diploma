from pathlib import Path
from typing import Dict, List, Union

import requests
from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer

from src.text_analyzers.common import RawTextProvider
from src.text_analyzers.runner import (
    Analyzer,
    Meta,
    Postprocessor,
    Preprocessor,
    ResultPublisher,
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
        sentiment_type, probability = [(key, value) for key, value in analyzer_output[0].items()][0]
        return Sentiment(probability=probability, type=sentiment_type)


class SentimentTextProvider(RawTextProvider):
    pass


class SentimentResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: Sentiment, meta: Meta):
        requests.post(self._url, params={"text_id": meta["id"]}, json=result.dict())
