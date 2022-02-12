from pathlib import Path

import pandas as pd
import requests

texts_csv_path = Path(__file__).resolve().parents[1] / "test_data.csv"


if __name__ == "__main__":

    texts_df = pd.read_csv(texts_csv_path)

    for _, row in texts_df.iterrows():
        data = {
            "text": row["text"],
            "source": row["source"],
        }
        response = requests.post("http://app:8000/text/add/", json=data)
        assert response.status_code == 200
