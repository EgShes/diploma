from pathlib import Path

import pytest

from src.text_analyzers.runner import Runner
from src.text_analyzers.sentiment.runner import (
    SentimentAnalyzer,
    SentimentPostprocessor,
    SentimentPreprocessor,
    SentimentResultPublisher,
)


@pytest.fixture(scope="session")
def sentiment_preprocessor() -> SentimentPreprocessor:
    return SentimentPreprocessor()


@pytest.fixture(scope="session")
def sentiment_analyzer(weights_path: Path) -> SentimentAnalyzer:
    return SentimentAnalyzer.load(weights_path / "sentiment/fasttext-social-network-model.bin")


@pytest.fixture(scope="session")
def sentiment_postprocessor() -> SentimentPostprocessor:
    return SentimentPostprocessor()


@pytest.fixture(scope="session")
def sentiment_publisher() -> SentimentResultPublisher:
    return SentimentResultPublisher("http://kek.com:8000")


@pytest.fixture(scope="session")
def sentiment_runner(
    sentiment_preprocessor, sentiment_analyzer, sentiment_postprocessor, sentiment_publisher
) -> Runner:
    return Runner(sentiment_preprocessor, sentiment_analyzer, sentiment_postprocessor, sentiment_publisher)


@pytest.fixture(scope="session")
def analyzer_input() -> str:
    return "Вася Иванов вчера в Испанию в командировку улетел, представляешь?"


@pytest.fixture()
def requests_mock(mocker):
    return mocker.Mock()
