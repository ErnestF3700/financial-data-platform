from datetime import datetime
from airflow.sdk import dag, task
from src.main import run_pipeline

@dag(
    dag_id="financial_etl",
    description="A DAG for financial ETL process",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["financial-data", "etl"],
)
def financial_etl():
    
    @task
    def run_etl():
        run_pipeline()
    run_etl()
    
financial_etl()