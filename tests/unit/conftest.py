from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def weights_path() -> Path:
    return Path(__file__).resolve().parents[2] / "weights"
