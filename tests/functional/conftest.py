import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://app:8000/"
