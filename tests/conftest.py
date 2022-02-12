import pytest


@pytest.fixture(scope="session")
def db_app_url() -> str:
    return "http://app:8000/"
