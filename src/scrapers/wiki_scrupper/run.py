import requests


def get_random_page() -> str:
    return "kek"


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/api/rest_v1/page/random/summary"
    response = requests.get(url)
    print(response.content)
    pass
