import pandas as pd
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.engine import Engine
from variables.config import REDSHIFT_SCHEMA

def insert_crypto_description_scd2(engine: Engine, crypto_description_df: pd.DataFrame) -> None:
    """
    Implement Slowly Changing Dimension (SCD) Type 2 in the 'crypto_description' table.

    Args:
        engine (Engine): SQLAlchemy engine for database connection.
        crypto_description_df (pd.DataFrame): DataFrame containing crypto data to be inserted.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    with engine.begin() as connection:
        rows_added = 0
        rows_updated = 0

        # Filtrar datos que no están en la base de datos
        existing_symbols = connection.execute(
            text(f'SELECT symbol FROM "{REDSHIFT_SCHEMA}".crypto_description WHERE is_current = 1')
        ).fetchall()

        existing_symbols_set = {row[0] for row in existing_symbols}

        # Filtrar el DataFrame para que solo contenga nuevos registros
        crypto_description_df = crypto_description_df[~crypto_description_df["symbol"].isin(existing_symbols_set)]

        if crypto_description_df.empty:
            print("No new records to insert; all records are already present in crypto_description.")
            return

        for _, row in crypto_description_df.iterrows():
            # Verificar si hay un registro existente actual para el símbolo de criptomonedas
            result = connection.execute(
                text(
                    f"""
                    SELECT * FROM "{REDSHIFT_SCHEMA}".crypto_description
                    WHERE symbol = :symbol AND is_current = 1
                    """
                ),
                {"symbol": row["symbol"]},
            )
            current_record = result.fetchone()

            if current_record:
                # Verificar si se han cambiado valores (excluyendo start_date, end_date, is_current)
                if (
                    row["name"] != current_record[1]
                    or row["category"] != current_record[3]
                    or row["description"] != current_record[4]
                    or row["bk_crypto"] != current_record[0]
                    or row["logo"] != current_record[6]
                    or row["website"] != current_record[7]
                    or row["reddit"] != current_record[8]
                ):
                    # Marcar el registro existente como no actual y establecer la fecha de finalización
                    connection.execute(
                        text(
                            f"""
                            UPDATE "{REDSHIFT_SCHEMA}".crypto_description
                            SET is_current = 0, end_date = :end_date
                            WHERE symbol = :symbol AND is_current = 1
                            """
                        ),
                        {
                            "end_date": datetime.now().date(),
                            "symbol": row["symbol"],
                        },
                    )
                    rows_updated += 1

                    # Insertar un nuevo registro con is_current = 1 y start_date = hoy
                    connection.execute(
                        text(
                            f"""
                            INSERT INTO "{REDSHIFT_SCHEMA}".crypto_description (
                                name, symbol, category, description, bk_crypto, logo, website, reddit,
                                start_date, end_date, is_current
                            ) VALUES (
                                :name, :symbol, :category, :description, :bk_crypto, :logo, :website, :reddit,
                                :start_date, :end_date, :is_current
                            )
                            """
                        ),
                        {
                            "name": row["name"],
                            "symbol": row["symbol"],
                            "category": row["category"],
                            "description": row["description"],
                            "bk_crypto": row["bk_crypto"],
                            "logo": row["logo"],
                            "website": row["website"],
                            "reddit": row["reddit"],
                            "start_date": datetime.now().date(),
                            "end_date": datetime.strptime("9999-12-01", "%Y-%m-%d").date(),
                            "is_current": 1,
                        },
                    )
                    rows_added += 1
            else:
                # Insertar un nuevo registro si no existe un registro actual
                connection.execute(
                    text(
                        f"""
                        INSERT INTO "{REDSHIFT_SCHEMA}".crypto_description (
                            name, symbol, category, description, bk_crypto, logo, website, reddit,
                            start_date, end_date, is_current
                        ) VALUES (
                            :name, :symbol, :category, :description, :bk_crypto, :logo, :website, :reddit,
                            :start_date, :end_date, :is_current
                        )
                        """
                    ),
                    {
                        "name": row["name"],
                        "symbol": row["symbol"],
                        "category": row["category"],
                        "description": row["description"],
                        "bk_crypto": row["bk_crypto"],
                        "logo": row["logo"],
                        "website": row["website"],
                        "reddit": row["reddit"],
                        "start_date": datetime.now().date(),
                        "end_date": datetime.strptime("9999-12-01", "%Y-%m-%d").date(),
                        "is_current": 1,
                    },
                )
                rows_added += 1

        # Imprimir el resultado de la operación
        if rows_updated > 0:
            print(f"Updated {rows_updated} records in crypto_description.")
        if rows_added > 0:
            print(f"Added {rows_added} new records to crypto_description.")
        if rows_added == 0 and rows_updated == 0:
            print("No records were added or updated in crypto_description.")

            
def insert_date_data(engine: Engine, dim_date_df: pd.DataFrame) -> None:
    """
    Insert new date records into the 'dim_date' without duplicating existing ones.

    Args:
        engine (Engine): SQLAlchemy engine for database connection.
        dim_date_df (pd.DataFrame): DataFrame containing date data to be inserted.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    with engine.connect() as connection:
        # Recuperar todas las fechas existentes en la tabla
        result = connection.execute(
            text(
                f"""
                SELECT date FROM "{REDSHIFT_SCHEMA}".dim_date
            """
            )
        )
        # Convertir las fechas obtenidas en un set para comparación rápida
        existing_dates_in_table = {row[0] for row in result.fetchall()}

        # Asegurarse de que la columna 'date' del DataFrame sea del tipo de fecha
        dim_date_df["date"] = pd.to_datetime(dim_date_df["date"]).dt.date

        # Filtrar el DataFrame para obtener solo las fechas que no están en la tabla
        new_dates_df = dim_date_df[~dim_date_df["date"].isin(existing_dates_in_table)]

        # Verificar si hay fechas nuevas para insertar
        if not new_dates_df.empty:
            # Insertar las nuevas fechas en la tabla
            new_dates_df.to_sql(
                "dim_date",
                con=connection,
                schema=f"{REDSHIFT_SCHEMA}",
                if_exists="append",
                index=False,
            )
            print(f"Added {len(new_dates_df)} new dates to dim_date.")
        else:
            print("No new dates were added; all dates are already present in dim_date.")
 
def insert_daily_crypto_prices(engine: Engine, daily_crypto_prices_df: pd.DataFrame) -> None:
    """
    Insert or update daily crypto prices data in the 'daily_crypto_prices'.

    Args:
        engine (Engine): SQLAlchemy engine for database connection.
        daily_crypto_prices_df (pd.DataFrame): DataFrame containing
            daily stock prices data to be inserted.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    
    with engine.begin() as connection:
        # Get the latest date from the daily_stock_prices_table
        result = connection.execute(
            text(
                f"""
                SELECT DISTINCT date
                FROM "{REDSHIFT_SCHEMA}".daily_crypto_prices
                """
            )
        )
        # Fetch all distinct dates into a set
        existing_dates_in_table = {row[0] for row in result.fetchall()}
        
        # Ensure the 'date' column in daily_crypto_prices_df is in date format
        daily_crypto_prices_df["date"] = pd.to_datetime(daily_crypto_prices_df["date"]).dt.date
        
        # Filter out rows where the date already exists in the table
        new_prices_df = daily_crypto_prices_df[~daily_crypto_prices_df["date"].isin(existing_dates_in_table)]
        
        # Insert only the new records
        if not new_prices_df.empty:
            new_prices_df.to_sql(
                "daily_crypto_prices",
                con=connection,
                schema=f"{REDSHIFT_SCHEMA}",
                if_exists="append",
                index=False,
            )
            print(f"Added {len(new_prices_df)} records to daily_crypto_prices.")
        else:
            print("No new records to add; they were already present in daily_crypto_prices.")