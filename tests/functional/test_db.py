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
        "chat/read/",
        "employee/read/",
    ],
)
def test_read_empty(db_app_url: str, url: str):
    response = requests.get(db_app_url + url, params={"ids": list(range(1, 10))})
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
    "json",
    [
        {"type": "kek"},
        {"type": ""},
    ],
)
def test_chat_wrong_input(db_app_url: str, json: Dict[str, Any]):
    response = requests.post(db_app_url + "chat/add", json=json)
    assert response.status_code == 422


@pytest.mark.parametrize("type_", ["direct", "group", "comments"])
def test_chat_addition(db_app_url: str, type_: str):
    response = requests.post(db_app_url + "chat/add", json={"type": type_})
    assert response.status_code == 200


def test_chat_read(db_app_url: str):
    response = requests.get(db_app_url + "chat/read", params={"ids": (1, 2, 3)})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize("passport", ["11111111", "22222222", "33333333"])
def test_employee_addition(db_app_url: str, passport: str):
    response = requests.post(
        db_app_url + "employee/add",
        json={"passport": passport, "first_name": "Oleg", "second_name": "Tinkoff", "department": "Director"},
    )
    assert response.status_code == 200


def test_employee_read(db_app_url: str):
    response = requests.get(db_app_url + "employee/read", params={"ids": (1, 2, 3)})
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "data",
    [
        {"text": "Россия - страна, где живет Дмитрий Медведев", "source": "vk", "chat_id": 1, "employee_id": 1},
        {
            "text": "В прошлые выходные в Москве прошли муниципальные выборы",
            "source": "vk",
            "chat_id": 2,
            "employee_id": 2,
        },
        {"text": "Ненавижу работать по вечерам", "source": "vk", "chat_id": 3, "employee_id": 3},
    ],
)
def test_text_addition(db_app_url: str, data: Dict[str, Any]):
    response = requests.post(db_app_url + "text/add/", json=data)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "data",
    [
        {"text": "text", "source": "vk", "chat_id": 100, "employee_id": 1},
        {"text": "text", "source": "vk", "chat_id": 2, "employee_id": 200},
    ],
)
def test_text_wrong_ids(db_app_url: str, data: Dict[str, Any]):
    response = requests.post(db_app_url + "text/add/", json=data)
    assert response.status_code == 404


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
