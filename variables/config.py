import os
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime, timedelta
import pytz

# Load environment variables from the .env file
DIR_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the timezone for Buenos Aires
BUENOS_AIRES_TIMEZONE = pytz.timezone('America/Argentina/Buenos_Aires')

# Get the current date and time in Buenos Aires timezone
HORA_BUENOS_AIRES: datetime = datetime.now(BUENOS_AIRES_TIMEZONE)

# Calculate the date for one day ago
YESTERDAY_FECHA: datetime = HORA_BUENOS_AIRES - timedelta(days=1)

# Format the date as a string in 'YYYY-MM-DD' format
DATE_STR: str = YESTERDAY_FECHA.strftime('%Y-%m-%d')

# List of cryptocurrencies -  CoinGecko - Public and Free API
COINS_LIST: List[str] = [
    "bitcoin",
    "ethereum",
    "cardano",
    "dogecoin",
    "axie-infinity",  # AXS
    "smooth-love-potion"  # SLP
]

# List of cryptocurrencies CoinMarketCap - API
coin_id: List[str] = [
    '1', #BTC (Bitcoin)
    '74', #DOGE (Dogecoin)
    '1027', #ETH (Ethereum)
    '2010', #ADA (Cardano)
    '5824', #SLP (Smooth Love Potion)
    '6783', #AXS (Axie Infinity)
    '31093' #DOGE (Dogecoin V2)
]

# API_COINMARKET_CAP # Cargar variables de entorno desde .env
load_dotenv()
API_KEY_COINMARKETCAP = os.getenv('api_key_coinmarketcap')

# Load Redshift database connection details from environment variables
DBNAME_REDSHIFT: Optional[str] = os.getenv('DBNAME_REDSHIFT')
USER_REDSHIFT: Optional[str] = os.getenv('USER_REDSHIFT')
PASSWORD_REDSHIFT: Optional[str] = os.getenv('PASSWORD_REDSHIFT')
HOST_REDSHIFT: Optional[str] = os.getenv('HOST_REDSHIFT')
PORT_REDSHIFT: Optional[str] = os.getenv('PORT_REDSHIFT')
REDSHIFT_SCHEMA: Optional[str] = os.getenv('REDSHIFT_SCHEMA')
