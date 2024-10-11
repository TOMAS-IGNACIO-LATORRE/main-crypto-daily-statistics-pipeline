import os
import time
import pandas as pd
from airflow.exceptions import AirflowException
from dotenv import load_dotenv
from staging.api_extract_data import (
    get_crypto_ohlc_data,
    create_crypto_table,
)
from variables.config import DIR_PATH, COINS_LIST, coin_id, API_KEY_COINMARKETCAP


def parquet_create_staging(date: str) -> None:
    """
    Creates Parquet files for daily cryptocurrency prices and cryptocurrency profiles.

    Args:
        date (str): The date for which the data is retrieved, in 'YYYY-MM-DD' format.
    
    Raises:
        AirflowException: If no valid data is retrieved for any cryptocurrency prices.
    """
    daily_crypto_prices_table = pd.DataFrame()
    crypto_table = pd.DataFrame()

    # Obtener precios diarios de criptomonedas y perfiles
    for coin in COINS_LIST:
        # Obtener precios diarios
        price_data = get_crypto_ohlc_data(coin, date)
        if not price_data.empty:
            daily_crypto_prices_table = pd.concat([daily_crypto_prices_table, price_data], ignore_index=True)
        else:
            print(f"No se encontraron datos de precios para la moneda: {coin}")
        time.sleep(15)  # Espera 15 segundos entre solicitudes

    for cid in coin_id:
        # Crear tabla de perfiles de criptomonedas
        profile_data = create_crypto_table(cid, API_KEY_COINMARKETCAP)
        if not profile_data.empty:
            crypto_table = pd.concat([crypto_table, profile_data], ignore_index=True)
        else:
            print(f"No se encontraron datos de perfil para el ID de moneda: {cid}")

    # Verificar si las tablas están vacías
    if daily_crypto_prices_table.empty:
        raise AirflowException("No se pudieron recuperar datos de precios diarios para ninguna moneda.")
    if crypto_table.empty:
        raise AirflowException("No se pudieron recuperar datos de perfil para ninguna moneda.")

    # Guardar precios diarios en un archivo Parquet
    daily_crypto_prices_file = os.path.join(DIR_PATH, "staging", "data", f"daily_crypto_prices_table_{date}_staging.parquet")
    daily_crypto_prices_table.to_parquet(daily_crypto_prices_file, index=False)
    print(f"Archivo '{daily_crypto_prices_file}' creado exitosamente.")

    # Guardar perfiles de criptomonedas en un archivo Parquet
    crypto_table_file = os.path.join(DIR_PATH, "staging", "data", f"crypto_table_{date}_staging.parquet")
    crypto_table.to_parquet(crypto_table_file, index=False)
    print(f"Archivo '{crypto_table_file}' creado exitosamente.")
