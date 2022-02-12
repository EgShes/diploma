import pytest
import requests


def test_text_added(db_app_url: str, texts_df: str):
    response = requests.get(db_app_url + "text/read/", params={"ids": list(range(50))})
    assert response.status_code == 200
    assert len(response.json()) == len(texts_df)


@pytest.mark.parametrize(
    "url",
    [
        "word/for_processing/",
        "named_entity/for_processing/",
        "sentiment/for_processing/",
    ],
)
def test_processed(db_app_url: str, url: str):
    response = requests.get(db_app_url + url, params={"n": 50})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "url,expected_num",
    [
        ("word/read/", 50),
        ("named_entity/read/", 33),
        ("sentiment/read/", 5),
    ],
)
def test_number_of_processed(db_app_url: str, url: str, expected_num: int):
    response = requests.get(db_app_url + url, params={"ids": list(range(1, 51))})
    print(response.content)
    assert response.status_code == 200
    assert len(response.json()) == expected_num
