import pandas as pd
from decimal import Decimal, InvalidOperation


REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "transaction_date",
    "status"
]

ALLOWED_STATUSES = ["completed", "pending", "failed"]


def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and validate financial transaction data.
    """
    # TODO 1: Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # TODO 2: Create a copy of DataFrame
    df_transformed = df.copy()
    
    # TODO 3: Convert transaction_date to datetime
    df_transformed['transaction_date'] = pd.to_datetime(df_transformed['transaction_date'], errors='raise')
    
    # TODO 4: Convert amount to Decimal
    def convert_to_decimal(value):
         try:
            amount = Decimal(str(value))
        
            if not amount.is_finite():
               raise ValueError(f"Amount must be a finite number. Found: {value}")
        
            if amount <= 0:
               raise ValueError("amount must be greater than 0")
            return amount
    
         except( InvalidOperation, TypeError, ValueError ) as exc:
            raise ValueError(f"Invalid amount value: {value}") from exc
    df_transformed['amount'] = df_transformed['amount'].apply(convert_to_decimal)
    
    # TODO 5: Normalize currency
    df_transformed['currency'] = df_transformed['currency'].str.strip().str.upper()
    
    # TODO 6: Validate status
    if not df_transformed['status'].isin(ALLOWED_STATUSES).all():
        raise ValueError(f"Invalid status found. Allowed statuses: {ALLOWED_STATUSES}")

    # TODO 7: Return transformed DataFrame
    return df_transformed