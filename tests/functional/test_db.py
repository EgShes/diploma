# Be careful! The order of tests matters
from typing import Any, Dict, List

import pytest
import requests


def test_health_check(db_app_url: str):
    response = requests.get(db_app_url + "health_check/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        "text/read/",
        "word/read/",
        "named_entity/read/",
        "sentiment/read/",
    ],
)
def test_read_empty(db_app_url: str, url: str):
    response = requests.get(db_app_url + url, params={"ids": list(range(-10, 10))})
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize(
    "url",
    [
        "word/for_processing/",
        "named_entity/for_processing/",
        "sentiment/for_processing/",
    ],
)
def test_for_processing_empty(db_app_url: str, url: str):
    response = requests.get(db_app_url + url, params={"n": 10})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "url",
    [
        "word/for_processing/",
        "named_entity/for_processing/",
        "sentiment/for_processing/",
    ],
)
@pytest.mark.parametrize("n", [-10, 0])
def test_for_processing_wrong_value(db_app_url: str, url: str, n: int):
    response = requests.get(db_app_url + url, params={"n": n})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "text",
    [
        "Россия - страна, где живет Дмитрий Медведев",
        "В прошлые выходные в Москве прошли муниципальные выборы",
        "Ненавижу работать по вечерам",
    ],
)
def test_text_addition(db_app_url: str, text: str):
    response = requests.post(db_app_url + "text/add/", json={"text": text, "source": "vk"})
    data = response.json()
    assert response.status_code == 200
    assert data["text"] == text
    assert data["source"] == "vk"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.parametrize(
    "url",
    [
        "word/for_processing/",
        "named_entity/for_processing/",
        "sentiment/for_processing/",
    ],
)
@pytest.mark.parametrize("n", [1, 2])
def test_for_processing_full(db_app_url: str, url: str, n: int):
    response = requests.get(db_app_url + url, params={"n": n})
    data = response.json()
    assert response.status_code == 200
    assert len(data) == n


@pytest.mark.parametrize(
    "url,params,data",
    [
        ("named_entity/add", {"text_id": 1}, {"text": "Россия", "type": "LOC"}),
        ("named_entity/add", {"text_id": 2}, {"text": "Дмитрий", "type": "PER"}),
        ("word/add", {"text_id": 1}, {"text": "живет", "quantity": 1}),
        ("word/add", {"text_id": 2}, {"text": "прошлые", "quantity": 1}),
        ("sentiment/add", {"text_id": 1}, {"type": "positive", "probability": 0.85}),
        ("sentiment/add", {"text_id": 2}, {"type": "negative", "probability": 0.65}),
    ],
)
def test_analysis_result_addition(db_app_url: str, url: str, params: Dict[str, Any], data: Dict[str, Any]):
    response = requests.post(db_app_url + url, params=params, json=data)
    assert response.status_code == 200
    assert len(response.json()) != 0


@pytest.mark.parametrize(
    "url,ids",
    [
        ("text/read/", [1, 2, 3]),
        ("word/read/", [1, 2]),
        ("named_entity/read/", [1, 2]),
        ("sentiment/read/", [1, 2]),
    ],
)
def test_read_full(db_app_url: str, url: str, ids: List[int]):
    response = requests.get(db_app_url + url, params={"ids": ids})
    assert response.status_code == 200
    assert len(response.json()) == len(ids)
