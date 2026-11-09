import pandas as pd
from src.load.postgres_loader import load_transactions
import pytest

def test_load_empty_dataframe():
    df = pd.DataFrame()
    result = load_transactions(df)
    assert result == 0
    
def test_load_duplicate_transaction_ids():
    df = pd.DataFrame([
        {
            "transaction_id": 90021,
            "customer_id": 501,
            "amount": 199.99,
            "currency": "PLN",
            "transaction_date": "2023-09-01 10:00:00",
            "status": "completed"
        },
        {
            "transaction_id": 90021,  # Duplicate transaction_id
            "customer_id": 502,
            "amount": 299.99,
            "currency": "PLN",
            "transaction_date": "2023-09-02 10:00:00",
            "status": "pending"
        }
    ])
    
   
    
    with pytest.raises(
        ValueError,
        match="Duplicate transaction IDs found in the DataFrame"
    ):
        load_transactions(df)
        
        
        
def test_load_missing_required_columns():
    df = pd.DataFrame([
        {
            "transaction_id": 90021,
            "customer_id": 501,
            "amount": 199.99,
            # Missing 'currency' column
            "transaction_date": "2023-09-01 10:00:00",
            "status": "completed"
        }
    ])
    
    with pytest.raises(
        ValueError,
        match="Missing required columns: {'currency'}"
    ):
        load_transactions(df)

def test_load_invalid_amount():
    df = pd.DataFrame([
        {
            "transaction_id": 90021,
            "customer_id": 501,
            "amount": -199.99,  # Invalid negative amount
            "currency": "PLN",
            "transaction_date": "2023-09-01 10:00:00",
            "status": "completed"
        }
    ])
    
    with pytest.raises(
        ValueError,
        match="Transaction amount must be greater than zero"
    ):
        load_transactions(df)
        
def test_load_invalid_currency_length():
    df = pd.DataFrame([
        {
            "transaction_id": 90021,
            "customer_id": 501,
            "amount": 199.99,
            "currency": "PL",  # Invalid currency length
            "transaction_date": "2023-09-01 10:00:00",
            "status": "completed"
        }
    ])
    
    with pytest.raises(
        ValueError,
        match="Currency must contain exactly 3 characters"
    ):
        load_transactions(df)
        
        
def test_load_invalid_status():
    df = pd.DataFrame([
        {
            "transaction_id": 90021,
            "customer_id": 501,
            "amount": 199.99,
            "currency": "PLN",
            "transaction_date": "2023-09-01 10:00:00",
            "status": "invalid_status"  # Invalid status
        }
    ])
    
    with pytest.raises(
        ValueError,
        match=r"Invalid transaction status. Valid statuses are:"
    ):
        load_transactions(df)