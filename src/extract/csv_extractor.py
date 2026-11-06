from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "transaction_date",
    "status"
]


def extract_csv(file_path: str) -> pd.DataFrame:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    df = pd.read_csv(file_path)
    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        raise ValueError(f"CSV file is missing required columns. Required: {REQUIRED_COLUMNS}")
    return df