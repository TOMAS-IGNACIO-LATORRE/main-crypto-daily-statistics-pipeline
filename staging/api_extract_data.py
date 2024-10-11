import pandas as pd
import requests
import time
from datetime import datetime
from typing import Dict, Optional


def get_crypto_ohlc_data(coin: str, date: str) -> pd.DataFrame:
    """
    Obtiene los precios OHLC de una criptomoneda para una fecha específica desde la API de CoinGecko.

    Args:
        coin (str): El nombre de la criptomoneda (e.g., 'ethereum', 'bitcoin').
        date (str): La fecha para la cual se obtienen los precios en formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Un DataFrame con las columnas 'date', 'time_hh_mm_ss', 'stock_symbol', 
                      'open_price', 'high_price', 'low_price', 'close_price', y 'volume'.
                      Devuelve un DataFrame vacío si no se encuentran datos.
    """
    # Definir la URL de la API y los parámetros para la solicitud. No es necesario API KEY porque es pública y gratuita dicha API
    API_URL = "https://api.coingecko.com/api/v3"
    COIN_OHLC = f"/coins/{coin}/ohlc"
    OHLC_PARAMS = {
        "vs_currency": "usd", # Indicamos la moneda en que queremos ver la cotización
        "days": 1  # Se puede ajustar según la API
    }

    url: str = API_URL + COIN_OHLC

    try:
        # Make a GET request to the REST API
        response: requests.Response = requests.get(url, params=OHLC_PARAMS)
        # Make sure the request was successful
        response.raise_for_status()
        # Python automáticamente convierte los json en diccionario
        data: Optional[Dict] = response.json()
    
    # Esta parte del código es un bloque de manejo de excepciones en Python, utilizado para gestionar errores que puedan ocurrir durante la ejecución
    # de una solicitud HTTP con la librería requests al aplicar el GET request. La variable e almacena el mensaje de error específico generado por la excepción.
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a la API de CoinGecko: {e}")
        return pd.DataFrame()

    # Crear una lista de diccionarios para almacenar las filas
    rows = []

    # Procesar los datos y crear las filas
    for price_info in data:
        # Obtener el timestamp y convertirlo a fecha
        timestamp = price_info[0]
        time = datetime.fromtimestamp(timestamp / 1000)
        
        # Filtrar los datos por la fecha especificada porque sino te trae los datos del día de hoy
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        
        if time.date() == target_date:
            # Crear un diccionario con la estructura solicitada
            row = {
                "date": time.date(),  # Agregar la fecha
                "time": time.strftime("%H:%M:%S"),  # Agregar el tiempo en formato hh:mm:ss
                "stock_symbol": coin,  # El nombre de la criptomoneda
                "open_price": float(price_info[1]),  # Precio de apertura
                "high_price": float(price_info[2]),  # Precio más alto
                "low_price": float(price_info[3]),  # Precio más bajo
                "close_price": float(price_info[4])  # Precio de cierre
            }
            rows.append(row)

    # Si no se encuentran datos para la fecha, retornar DataFrame vacío
    if not rows:
        print(f"No se encontraron datos de {coin} para la fecha {date}.")
        return pd.DataFrame()

    # Crear DataFrame a partir de la lista de diccionarios
    return pd.DataFrame(rows)

# Traemos los datos descriptivos de cada una de las coins elegidas para analizar
def create_crypto_table(coin_id: str, api_key: str) -> pd.DataFrame:
    url: str = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id={coin_id}"

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    try:
        response: requests.Response = requests.get(url, headers=headers)
        response.raise_for_status()
        data: Dict = response.json()

        if 'data' not in data or coin_id not in data['data']:
            print(f"Datos no disponibles para el ID de moneda {coin_id}.")
            return pd.DataFrame()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:  # Too Many Requests
            print("Demasiadas solicitudes. Esperando antes de reintentar...")
            time.sleep(60)  # Esperar 1 minuto
            return create_crypto_table(coin_id, api_key)  # Reintentar la solicitud
        else:
            print(f"Error al realizar la solicitud a la API de CoinMarketCap: {e}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error general: {e}")
        return pd.DataFrame()

    coin_info = data['data'][coin_id]
    result = {
        'symbol': coin_info['symbol'],
        'id': coin_info['id'],
        'name': coin_info['name'],
        'category': coin_info.get('category', 'No disponible'),
        'description': coin_info['description'],
        'logo': coin_info['logo'],
        'website': coin_info['urls']['website'][0] if coin_info['urls']['website'] else 'No disponible',
        'reddit': coin_info['urls'].get('reddit', ['No disponible'])[0] if coin_info['urls'].get('reddit') else 'No disponible'
    }

    return pd.DataFrame([result])