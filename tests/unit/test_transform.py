from src.extract.csv_extractor import extract_csv
from src.transform.transaction_transformer import transform_transactions


def test_transform_transactions():
    df = extract_csv("data/raw/transactions.csv")

    transformed = transform_transactions(df)

    assert len(transformed) == 5
    assert transformed["amount"].iloc[0].__class__.__name__ == "Decimal"
    assert transformed["transaction_date"].notna().all()