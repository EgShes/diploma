import re
from collections import Counter
from pathlib import Path
from typing import List, Set

import requests
from nltk.corpus import stopwords
from pydantic import BaseModel
from pymystem3 import Mystem

from src.text_analyzers.runner import (
    Analyzer,
    Meta,
    Postprocessor,
    Preprocessor,
    ResultPublisher,
)


class WordSchema(BaseModel):
    text: str
    quantity: int


class WordPreprocessor(Preprocessor):
    def __init__(self):
        self._punctuation_pattern = re.compile(r"[^\w\s]")
        self._newline_pattern = re.compile(r"\n")
        self._spaces_patter = re.compile(r"\s+")

    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def preprocess(self, text: str):
        text = text.lower()
        text = re.sub(self._punctuation_pattern, "", text)
        text = re.sub(self._newline_pattern, " ", text)
        text = re.sub(self._spaces_patter, " ", text)
        return text


class WordAnalyzer(Analyzer):
    def __init__(self, stemmer: Mystem, tokens2filter: Set[str]):
        self._stemmer = stemmer
        self._tokens2filter = tokens2filter

    @classmethod
    def load(cls, mystem_path: Path):
        # stemmer = Mystem(str(mystem_path))
        # TODO fix it
        stemmer = Mystem()
        tokens2filter = set(stopwords.words("russian") + [""])
        return cls(stemmer, tokens2filter)

    def analyze(self, text: str) -> List[str]:
        return [token.strip() for token in self._stemmer.lemmatize(text) if token.strip() not in self._tokens2filter]


class WordPostprocessor(Postprocessor):
    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def postprocess(self, analyzer_output: List[str]) -> List[WordSchema]:
        return [WordSchema(text=word, quantity=count) for word, count in Counter(analyzer_output).items()]


class WordResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: List[WordSchema], meta: Meta):
        for word in result:
            requests.post(self._url, params={"text_id": meta.id}, json=word.dict())
