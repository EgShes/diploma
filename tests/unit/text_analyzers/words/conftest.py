from pathlib import Path

import pytest

from src.text_analyzers.runner import Runner
from src.text_analyzers.words.runner import (
    WordAnalyzer,
    WordPostprocessor,
    WordPreprocessor,
    WordResultPublisher,
)


@pytest.fixture(scope="session")
def word_preprocessor() -> WordPreprocessor:
    return WordPreprocessor()


@pytest.fixture(scope="session")
def word_analyzer(weights_path: Path) -> WordAnalyzer:
    return WordAnalyzer.load(weights_path / "words/mystem-3.1-linux-64bit.tar.gz")


@pytest.fixture(scope="session")
def word_postprocessor() -> WordPostprocessor:
    return WordPostprocessor()


@pytest.fixture(scope="session")
def word_publisher() -> WordResultPublisher:
    return WordResultPublisher("http://kek.com:8000")


@pytest.fixture(scope="session")
def word_runner(word_preprocessor, word_analyzer, word_postprocessor, word_publisher) -> Runner:
    return Runner(word_preprocessor, word_analyzer, word_postprocessor, word_publisher)
