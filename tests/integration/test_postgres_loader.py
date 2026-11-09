import pandas as pd
from sqlalchemy import text
from decimal import Decimal
from src.load.postgres_loader import load_transactions
from src.config.database import engine
import pytest

@pytest.fixture
def cleanup_transactions():
    transaction_id = 90021  
    
    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM raw.transactions WHERE transaction_id = :transaction_id"),
            {"transaction_id": transaction_id}
        )
        
    yield transaction_id
    
    with engine.begin() as connection:
        connection.execute(
            text("""
                 DELETE FROM raw.transactions WHERE transaction_id = :transaction_id"""),
            {"transaction_id": transaction_id}
        )
        
        
        
def test_load_transactions(cleanup_transactions):
    df = pd.DataFrame([
        {
        "transaction_id": cleanup_transactions,
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
                 WHERE transaction_id = :transaction_id
            """),
            {"transaction_id": cleanup_transactions}
        ).fetchone()
        
    assert transaction.amount == Decimal("199.99")
    assert transaction.transaction_id == cleanup_transactions
    assert transaction.status == "completed"
    
    updated_df = pd.DataFrame([
        {
            "transaction_id": cleanup_transactions,
            "customer_id": 501,
            "amount": 299.99,
            "currency": "PLN",
            "transaction_date": "2023-09-01 10:00:00",
            "status": "completed"
        }
    ])

    # Aktualizacja istniejącego rekordu
    result = load_transactions(updated_df)
    assert result == 1

    # Ponowne załadowanie identycznych danych
    result = load_transactions(updated_df)
    assert result == 0

    with engine.connect() as connection:
        transaction = connection.execute(
            text("""
                SELECT transaction_id, amount, status
                FROM raw.transactions
                WHERE transaction_id = :transaction_id
            """),
            {"transaction_id": cleanup_transactions}
        ).fetchone()
    assert transaction.transaction_id == cleanup_transactions
    assert transaction.amount == Decimal("299.99")
    assert transaction.status == "completed"