import pandas as pd
import pytest
from src.extract.csv_extractor import extract_csv 

def test_extract_csv():
    df = extract_csv("data/raw/transactions.csv")
    assert isinstance(df, pd.DataFrame)
    get_required_columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "currency",
        "transaction_date",
        "status"
    ]
    for col in get_required_columns:
        assert col in df.columns
        
def test_extract_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_csv("data/raw/nonexistent.csv")
        
def test_extract_csv_missing_columns(tmp_path):
    csv_file = tmp_path / "invalid.csv"

    csv_file.write_text(
        "transaction_id,customer_id,amount\n"
        "1001,501,249.99\n"
    )

    with pytest.raises(ValueError):
        extract_csv(str(csv_file))