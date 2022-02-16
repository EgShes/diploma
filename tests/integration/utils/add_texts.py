from pathlib import Path

import pandas as pd
import requests

url = "http://app:8000/"
data_path = Path(__file__).resolve().parents[1] / "data"


def add_data(url: str, df_path: Path):
    df = pd.read_csv(df_path)

    for _, row in df.iterrows():
        response = requests.post(url, json=dict(row))
        assert response.status_code == 200


if __name__ == "__main__":
    add_data(url + "chat/add/", data_path / "chats.csv")
    add_data(url + "employee/add/", data_path / "employees.csv")
    add_data(url + "text/add/", data_path / "texts.csv")
