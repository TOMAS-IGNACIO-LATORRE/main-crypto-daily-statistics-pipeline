from sqlalchemy.engine import Engine
from variables.connection_redshift import create_redshift_engine
from Silver.create_tables_redshift import create_tables
from Silver.parquet_Silver import load_parquet_files
from Silver.table_insert_sql import (
    insert_crypto_description_scd2,
    insert_date_data,
    insert_daily_crypto_prices
)
import pandas as pd


def run_silver(**context) -> None:
    """
    Run the silver layer process, which includes creating tables,
    loading Parquet files, and inserting data into Redshift tables.

    Steps:
        1. Create necessary tables in the Redshift database.
        2. Load data from Parquet files.
        3. Insert stock, date, and daily stock prices data into Redshift.

    Raises:
        Exception: If there are issues with any of the steps,
        it will propagate the exception.
    """
    
    conn: Engine = create_redshift_engine()

    # Step 1: Create tables in the Redshift database if they don't exist
    create_tables(conn)

    # Step 2: Load Parquet files into DataFrames
    daily_crypto_prices_df: pd.DataFrame
    crypto_description_df: pd.DataFrame
    dim_date_df: pd.DataFrame
    daily_crypto_prices_df, crypto_description_df, dim_date_df = load_parquet_files(context["ds"])

    # Step 3: Insert data into Redshift tables
    insert_crypto_description_scd2(conn, crypto_description_df)
    insert_date_data(conn, dim_date_df)
    insert_daily_crypto_prices(conn, daily_crypto_prices_df)

if __name__ == "__main__":
    run_silver()