import logging
from typing import Tuple

import requests

from src.database.models import TextRead
from src.text_analyzers.runner import Meta, TextProvider


class RequestFailedException(Exception):
    pass


class RawTextProvider(TextProvider):
    def __init__(self, url: str):
        self._url = url

    def __iter__(self):
        self._counter = 1
        return self

    def __next__(self) -> Tuple[str, Meta]:
        try:
            response = requests.get(self._url, params={"text_id": self._counter})
            self._counter += 1
            if response.status_code != 200:
                raise RequestFailedException(
                    f'Got response code {response.status_code} with message {response.content.decode("utf-8")}'
                )
            data = TextRead.parse_raw(response.content)
            return data.raw_text, {"id": data.id}
        except Exception as e:
            logging.error(e)
            raise StopIteration from e
