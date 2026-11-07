from src.extract.csv_extractor import extract_csv
from src.transform.transaction_transformer import transform_transactions
from src.load.postgres_loader import load_transactions
from src.utils.logging_config import setup_logger

logger = setup_logger()
def run_pipeline():
    
    try: 
        logger.info("Starting ETL pipeline...")
        # Extract
        df = extract_csv("data/raw/transactions.csv")
        logger.info(f"Extracted {len(df)} transactions")
        # Transform
        transformed_df = transform_transactions(df)
        logger.info(f"Transformed {len(transformed_df)} transactions")
        # Load
        load_count = load_transactions(transformed_df)
        logger.info(f"loaded {load_count} transactions into the database.")

        logger.info("ETL pipeline completed successfully.")    
        
    except Exception:
        logger.exception("ETL pipeline failed.")
        raise

if __name__ == "__main__":
    run_pipeline()

       
    
    
