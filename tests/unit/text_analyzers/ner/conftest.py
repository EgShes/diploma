from pathlib import Path

import pytest

from src.text_analyzers.ner.runner import (
    NerAnalyzer,
    NerPostprocessor,
    NerPreprocessor,
    NerResultPublisher,
)
from src.text_analyzers.runner import Runner


@pytest.fixture(scope="session")
def ner_preprocessor() -> NerPreprocessor:
    return NerPreprocessor()


@pytest.fixture(scope="session")
def ner_analyzer(weights_path: Path) -> NerAnalyzer:
    return NerAnalyzer.load(
        weights_path / "ner/navec_news_v1_1B_250K_300d_100q.tar",
        weights_path / "ner/slovnet_ner_news_v1.tar",
    )


@pytest.fixture(scope="session")
def ner_postprocessor() -> NerPostprocessor:
    return NerPostprocessor()


@pytest.fixture(scope="session")
def ner_publisher() -> NerResultPublisher:
    return NerResultPublisher("http://kek.com:8000")


@pytest.fixture(scope="session")
def ner_runner(ner_preprocessor, ner_analyzer, ner_postprocessor, ner_publisher) -> Runner:
    return Runner(ner_preprocessor, ner_analyzer, ner_postprocessor, ner_publisher)


@pytest.fixture(scope="session")
def analyzer_input() -> str:
    return "Вася Иванов вчера в Испанию в командировку улетел, представляешь?"


@pytest.fixture()
def requests_mock(mocker):
    return mocker.Mock()
