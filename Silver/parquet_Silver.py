import pandas as pd
import os
from typing import Tuple
from variables.config import DIR_PATH

def load_parquet_files(date: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load and update Parquet files for daily crypto prices, crypto data, and dates.

    Args:
        date (str): The date string used for identifying the Parquet files.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        DataFrames for daily crypto prices, crypto data, and date information.

    Raises:
        Exception: If there is an error in processing the Parquet files.
    """

    # Paths for daily crypto prices
    daily_crypto_prices_path = os.path.join(DIR_PATH,"staging","data",f"daily_crypto_prices_table_{date}_staging.parquet",)
    daily_silver_path = os.path.join(DIR_PATH, "Silver", "data", "daily_crypto_prices_silver.parquet")
        
    # Load daily crypto prices DataFrame
    daily_crypto_prices_df = pd.read_parquet(daily_crypto_prices_path)
    daily_crypto_prices_df = daily_crypto_prices_df.rename(columns={"stock_symbol": "symbol"})
    
    # Reemplazar valores en la columna 'symbol'
    replacement_dict = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'cardano': 'ADA',
    'dogecoin': 'DOGE',
    'axie-infinity': 'AXS',
    'smooth-love-potion': 'SLP'
    }
    
    daily_crypto_prices_df['symbol'] = daily_crypto_prices_df['symbol'].replace(replacement_dict)

    # Check if Silver file exists and update it
    if os.path.exists(daily_silver_path):
        existing_daily_df = pd.read_parquet(daily_silver_path)
        new_data = daily_crypto_prices_df[
            ~daily_crypto_prices_df["date"].isin(existing_daily_df["date"])
        ]

        if not new_data.empty:
            daily_crypto_prices_df = pd.concat(
                [existing_daily_df, new_data], ignore_index=True
            )
            daily_crypto_prices_df.to_parquet(daily_silver_path, index=False)
            print("New data added to daily_crypto_prices_table_silver.")
        else:
            print("No new data added to daily_crypto_prices_table_silver; data for these dates already exists.")
    else:
        daily_crypto_prices_df.to_parquet(daily_silver_path, index=False)
        print("File daily_crypto_prices_table_silver created with initial data.")


    # Paths for crypto data
    crypto_path = os.path.join(DIR_PATH, "staging", "data", f"crypto_table_{date}_staging.parquet")
    crypto_silver_path = os.path.join(DIR_PATH, "Silver", "data", "crypto_table_silver.parquet")

    # Load crypto data DataFrame
    crypto_description_df = pd.read_parquet(crypto_path)
    crypto_description_df = crypto_description_df.rename(columns={"id": "bk_crypto"})
    
    # Check if Silver file exists and update it
    if os.path.exists(crypto_silver_path):
        existing_crypto_df = pd.read_parquet(crypto_silver_path)
        
        if not crypto_description_df.empty:
            
            # Merge with indicator to find new rows
            merged_df = pd.merge(
            crypto_description_df, 
            existing_crypto_df, 
            on=['bk_crypto', 'symbol', 'name', 'category', 'logo', 'website', 'reddit'], 
            how='left', 
            indicator=True
            )
            
            # Concatenar los nuevos datos con los datos existentes
            new_data = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
            
            rows_to_add = new_data.shape[0]
            if rows_to_add > 0:
                # Concatenar y guardar
                combined_crypto_df = pd.concat([existing_crypto_df, new_data], ignore_index=True)
                combined_crypto_df.to_parquet(crypto_silver_path, index=False)
                print(f"New data added to crypto_table_silver: {rows_to_add} rows.")

        else:
            print("No new data added to crypto_table_silver; data for these rows already exists.")
    else:
        crypto_description_df.to_parquet(crypto_silver_path, index=False)
        print("File crypto_table_silver created with initial data.")
    
        # Generate date DataFrame with correct dim_date structure
    unique_dates = pd.to_datetime(daily_crypto_prices_df["date"]).dt.date.unique()

    dim_date_df = pd.DataFrame(pd.to_datetime(unique_dates), columns=["date"])
    dim_date_df["year"] = dim_date_df["date"].apply(lambda x: x.year)
    dim_date_df["month"] = dim_date_df["date"].apply(lambda x: x.month)
    dim_date_df["week_number"] = dim_date_df["date"].apply(lambda x: x.isocalendar()[1])
    dim_date_df["day"] = dim_date_df["date"].apply(lambda x: x.day)
    dim_date_df["yearmonth"] = dim_date_df["date"].apply(lambda x: x.strftime("%Y%m"))
    dim_date_df["month_name"] = dim_date_df["date"].apply(lambda x: x.strftime("%B"))
    dim_date_df["day_of_week"] = dim_date_df["date"].apply(lambda x: x.weekday() + 1)  # Monday=1, Sunday=7
    dim_date_df["day_of_year"] = dim_date_df["date"].apply(lambda x: x.timetuple().tm_yday)
    dim_date_df["week_of_year"] = dim_date_df["date"].apply(lambda x: x.isocalendar()[1])
    dim_date_df["quarter"] = dim_date_df["date"].apply(lambda x: (x.month - 1) // 3 + 1)
    dim_date_df["semester"] = dim_date_df["date"].apply(lambda x: 1 if x.month <= 6 else 2)
    dim_date_df["is_weekend"] = dim_date_df["date"].apply(lambda x: x.weekday() >= 5)
    
    # Paths for date table
    date_silver_path = os.path.join(DIR_PATH, "Silver", "data", "date_table_silver.parquet")

    # Check if Silver file exists and update it
    if os.path.exists(date_silver_path):
        existing_date_df = pd.read_parquet(date_silver_path)
        new_dates = dim_date_df[~dim_date_df["date"].isin(existing_date_df["date"])]

        if not new_dates.empty:
            dim_date_df = pd.concat([existing_date_df, new_dates], ignore_index=True)
            dim_date_df.to_parquet(date_silver_path, index=False)
            print("New dates added to date_table_silver.")
        else:
            print("No new dates added to date_table_silver; dates already exist.")
    else:
        dim_date_df.to_parquet(date_silver_path, index=False)
        print("File date_table_silver created with initial dates.")

    return daily_crypto_prices_df, crypto_description_df, dim_date_df
    
