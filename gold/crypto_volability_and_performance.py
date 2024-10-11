import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from variables.config import REDSHIFT_SCHEMA

def calculate_crypto_volability_and_performance(engine: Engine, date: str) -> None:
    """
    Calculate financial attributes for the 'crypto' layer based on daily crypto data
    and insert the results into the 'crypto_volatility_and_performance' table in the database.
    
    Args:
        engine (Engine): SQLAlchemy engine for database connection.
        date (str): Date for which the crypto attributes are calculated.

    Raises:
        Exception: If there is an issue with the database query or insertion.
    """

    with engine.begin() as connection:
        # Check if the date already exists in the crypto_volatility_and_performance table
        check_query = text(f"""
            SELECT 1 FROM "{REDSHIFT_SCHEMA}".crypto_volatility_and_performance
            WHERE date = :date
            LIMIT 1
        """)
        result = connection.execute(check_query, {'date': date}).fetchone()

        if result:
            print(f"Data for the date {date} already exists. No new calculations were made in crypto_volatility_and_performance.")
            return

        # Read data from daily_crypto_prices for the given date and join with crypto_description to get the category
        query = text(f"""
            SELECT
                dp.date,
                dp.symbol,
                dp.open_price,
                dp.high_price,
                dp.low_price,
                dp.close_price,
                cd.category
            FROM "{REDSHIFT_SCHEMA}".daily_crypto_prices dp
            LEFT JOIN "{REDSHIFT_SCHEMA}".crypto_description cd
            ON dp.symbol = cd.symbol
            WHERE dp.date = :date
            AND cd.is_current = 1
        """)
        df = pd.read_sql_query(query, connection, params={'date': date})

        if df.empty:
            print(f"No data available for the {date}.")
            return

        # Calculate daily metrics
        metrics = df.groupby(['date', 'symbol', 'category']).agg(
            low_price=('low_price', 'min'),
            high_price=('high_price', 'max'),
            open_price=('open_price', 'first'),
            close_price=('close_price', 'last'),
            average_price=('close_price', 'mean'),
            standard_desviation=('close_price', 'std'),
        ).reset_index()

        # Calculate additional metrics
        metrics['volatility'] = (metrics['high_price'] - metrics['low_price']) / metrics['close_price']
        metrics['return'] = (metrics['close_price'] - metrics['open_price']) / metrics['open_price'] * 100
        metrics['range'] = metrics['high_price'] - metrics['low_price']
        metrics['time_interval'] = 'daily'

        # Prepare the DataFrame for insertion
        metrics = metrics[['date', 'symbol', 'category', 'time_interval', 'low_price', 'high_price', 
                           'volatility', 'open_price', 'close_price', 'return', 'range', 
                           'average_price', 'standard_desviation']]

        # Insert calculated metrics into the 'crypto_volatility_and_performance' table
        metrics.to_sql(
            'crypto_volatility_and_performance',
            con=connection,
            schema=f'{REDSHIFT_SCHEMA}',
            if_exists='append',
            index=False
        )

        # Log the successful insertion of calculated attributes
        print(f"KPIs successfully inserted for the date {date}.")
