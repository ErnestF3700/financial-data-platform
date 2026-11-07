import pandas as pd
from src.load.postgres_loader import load_transactions


def test_load_empty_dataframe():
    df = pd.DataFrame()
    result = load_transactions(df)
    assert result == 0