import re
from typing import List, Set

from nltk.corpus import stopwords
from pymystem3 import Mystem

from src.text_analyzers.common import RawTextProvider
from src.text_analyzers.runner import (
    Analyzer,
    Meta,
    Postprocessor,
    Preprocessor,
    ResultPublisher,
    Runner,
)


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
    def load(cls, *args, **kwargs):
        stemmer = Mystem()
        tokens2filter = set(stopwords.words("russian") + [""])
        return cls(stemmer, tokens2filter)

    def analyze(self, text: str) -> List[str]:
        return [token.strip() for token in self._stemmer.lemmatize(text) if token.strip() not in self._tokens2filter]


class WordPostprocessor(Postprocessor):
    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def postprocess(self, analyzer_output: List[str]):
        return analyzer_output


class WordTextProvider(RawTextProvider):
    pass


class WordResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: str, meta: Meta):
        pass


if __name__ == "__main__":

    preprocessor = WordPreprocessor()
    analyzer = WordAnalyzer.load()
    postprocessor = WordPostprocessor()
    text_provider = WordTextProvider(url="http://0.0.0.0:8080/text")
    result_publisher = WordResultPublisher(url="http://0.0.0.0:8080/ner")

    runner = Runner(preprocessor, analyzer, postprocessor, text_provider, result_publisher)

    runner.run()
