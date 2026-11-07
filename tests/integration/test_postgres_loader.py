import pandas as pd
from sqlalchemy import text

from src.load.postgres_loader import load_transactions
from src.config.database import engine

def test_load_transactions():
    df = pd.DataFrame([
        {
        "transaction_id": 9001,
        "customer_id": 501,
        "amount": 199.99,
        "currency": "PLN",
        "transaction_date": "2023-09-01 10:00:00",
        "status": "completed"
      }
    ])
    
    result = load_transactions(df)
    
    assert result == 1
    
    with engine.connect() as connection:
        transaction = connection.execute(
            text("""
                 SELECT transaction_id, amount, status
                 FROM raw.transactions
                 WHERE transaction_id = 9001
            """)
        ).fetchone()
        
    assert transaction is not None
    assert transaction.transaction_id == 9001
    assert transaction.status == "completed"