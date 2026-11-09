import pandas as pd
from sqlalchemy import text

from src.config.database import engine



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
    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction IDs found in the DataFrame")
    records = df.to_dict(orient="records")

    with engine.begin() as connection:
        result = connection.execute(INSERT_QUERY, records)
    return result.rowcount