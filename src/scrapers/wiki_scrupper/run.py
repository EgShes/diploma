import json
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import count
from random import choice
from time import sleep

import requests
from tqdm import tqdm

WIKI_RANDOM_PAGE_URL = "https://ru.wikipedia.org/api/rest_v1/page/random/summary"
TEXT_RETRY_SECONDS = 1


class WikiPageNotAvailableError(Exception):
    pass


class TextNotInserted(Exception):
    pass


@dataclass
class WikiText:
    title: str
    text: str


def get_random_page() -> WikiText:
    response = requests.get(WIKI_RANDOM_PAGE_URL)
    if response.status_code != 200:
        raise WikiPageNotAvailableError
    page = json.loads(response.content)
    return WikiText(page["title"], page["extract"])


def post_text(wiki_text: WikiText, url: str, chat_id: int, employee_id: int):
    response = requests.post(
        url, json={"text": wiki_text.text, "source": "wiki", "employee_id": employee_id, "chat_id": chat_id}
    )
    if response.status_code != 200:
        raise TextNotInserted


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "--max",
        type=int,
        default=-1,
        help="Number of texts to put to database. -1 if no upper limit",
    )
    parser.add_argument("--ip", type=str, default="http://0.0.0.0", help="Ip of db api")
    parser.add_argument("--port", type=int, default=8080, help="Port of db api")
    parser.add_argument("--chat_ids", nargs="+", type=int, default=(1, 2, 3), help="Ids of chats to add to")
    parser.add_argument("--employee_ids", nargs="+", type=int, default=(1, 2, 3), help="Ids of employees to add to")
    args = parser.parse_args()

    url = f"{args.ip}:{args.port}/text/add/"

    for i in tqdm(count()):
        try:
            text = get_random_page()
            post_text(text, url, choice(args.chat_ids), choice(args.employee_ids))
            if args.max != -1 and i == args.max:
                break
        except WikiPageNotAvailableError:
            logging.warning(f"Could not get random wiki page. Retrying in {TEXT_RETRY_SECONDS}")
            sleep(TEXT_RETRY_SECONDS)
        except TextNotInserted:
            logging.warning(f"Could not put text to database. Retrying in {TEXT_RETRY_SECONDS}")
            sleep(TEXT_RETRY_SECONDS)
    logging.info("Finished")
