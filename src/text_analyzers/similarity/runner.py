import re
from pathlib import Path
from typing import List, Union

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from src.text_analyzers.common import RawTextProvider
from src.text_analyzers.runner import (
    Analyzer,
    Meta,
    Postprocessor,
    Preprocessor,
    ResultPublisher,
    Runner,
)


class SimilarityPreprocessor(Preprocessor):
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


class SimilarityAnalyzer(Analyzer):
    def __init__(self, model_name: str, device: str, weights_folder):
        self._model = SentenceTransformer(model_name_or_path=model_name, device=device, cache_folder=weights_folder)

    @classmethod
    def load(cls, weight_folder: Union[str, Path], device: str = "cpu"):
        return cls(
            model_name="symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli",
            device=device,
            weights_folder=weight_folder,
        )

    @torch.no_grad()
    def analyze(self, text: str) -> List[np.ndarray]:
        return self._model.encode([text])


class SimilarityPostprocessor(Postprocessor):
    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

    def postprocess(self, analyzer_output: List[np.ndarray]) -> List[np.ndarray]:
        return analyzer_output


class SimilarityTextProvider(RawTextProvider):
    pass


class SimilarityResultPublisher(ResultPublisher):
    def __init__(self, url: str):
        self._url = url

    def publish(self, result: List[np.ndarray], meta: Meta):
        pass


if __name__ == "__main__":

    preprocessor = SimilarityPreprocessor()
    analyzer = SimilarityAnalyzer.load(weight_folder="/home/egor/.cache/torch/sentence_transformers")
    postprocessor = SimilarityPostprocessor()
    text_provider = SimilarityTextProvider(url="http://0.0.0.0:8080/text")
    result_publisher = SimilarityResultPublisher(url="http://0.0.0.0:8080/ner")

    runner = Runner(preprocessor, analyzer, postprocessor, text_provider, result_publisher)

    runner.run()
