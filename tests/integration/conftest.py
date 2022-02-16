from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def texts_df() -> pd.DataFrame:
    texts_csv_path = Path(__file__).resolve().parent / "data" / "texts.csv"
    return pd.read_csv(texts_csv_path)
