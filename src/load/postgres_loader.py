import pandas as pd
from sqlalchemy import text

from src.config.database import engine
VALID_STATUSES = {"completed", "pending", "failed"}
REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "transaction_date",
    "status"
]

INSERT_QUERY = text("""
    INSERT INTO raw.transactions (
        transaction_id,
        customer_id,
        amount,
        currency,
        transaction_date,
        status
    )
    VALUES (
        :transaction_id,
        :customer_id,
        :amount,
        :currency,
        :transaction_date,
        :status
    )
   ON CONFLICT (transaction_id)
DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    amount = EXCLUDED.amount,
    currency = EXCLUDED.currency,
    transaction_date = EXCLUDED.transaction_date,
    status = EXCLUDED.status
WHERE
    (raw.transactions.customer_id,
     raw.transactions.amount,
     raw.transactions.currency,
     raw.transactions.transaction_date,
     raw.transactions.status)
    IS DISTINCT FROM
    (EXCLUDED.customer_id,
     EXCLUDED.amount,
     EXCLUDED.currency,
     EXCLUDED.transaction_date,
     EXCLUDED.status)
""")


def load_transactions(df: pd.DataFrame) ->int:     
    
    if df is None or df.empty:
        return 0
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns) 
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    if (df["amount"] <= 0).any():
        raise ValueError("Transaction amount must be greater than zero")
    if (df["currency"].str.len() != 3).any():
        raise ValueError("Currency must contain exactly 3 characters")
    if not df["status"].isin(VALID_STATUSES).all():
        raise ValueError(f"Invalid transaction status. Valid statuses are: {sorted(VALID_STATUSES)}")
    if pd.to_datetime(df["transaction_date"], errors='coerce').isna().any():
        raise ValueError("Invalid transaction date")
    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction IDs found in the DataFrame")
    records = df.to_dict(orient="records")

    with engine.begin() as connection:
        result = connection.execute(INSERT_QUERY, records)
    return result.rowcount