from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def weights_path() -> Path:
    return Path(__file__).resolve().parents[2] / "weights"


@pytest.fixture()
def requests_mock(mocker):
    return mocker.Mock()


@pytest.fixture(scope="session")
def analyzer_input() -> str:
    return "Вася Иванов вчера в Испанию в командировку улетел, представляешь?"
