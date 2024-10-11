from sqlalchemy import text
from sqlalchemy.engine import Engine


def create_tables(engine: Engine) -> None:
    """
    Create tables in the Redshift database if they do not exist.

    Args:
        engine (Engine): SQLAlchemy engine for the database connection.
    """

    def table_exists(table_name: str) -> bool:
        """
        Check if a table exists in the database schema.

        Args:
            table_name (str): Name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """

        with engine.connect() as connection:
            query = text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = '2024_tomas_ignacio_latorre_schema'
                    AND table_name = :table_name
                )
                """
            )
            result = connection.execute(query, {"table_name": table_name})
            return result.fetchone()[0]

    with engine.connect() as connection:
        # Create crypto_description table if it does not exist
        if not table_exists("crypto_description"):
            connection.execute(
                text(
                    """
                    CREATE TABLE "2024_tomas_ignacio_latorre_schema".crypto_description (
                        id_crypto BIGINT IDENTITY(1,1) PRIMARY KEY, 
                        name VARCHAR(100) NOT NULL, 
                        symbol VARCHAR(10) NOT NULL UNIQUE,  
                        category VARCHAR(50),  
                        description VARCHAR(8192),  
                        bk_crypto BIGINT,  
                        logo VARCHAR(8192),   
                        website VARCHAR(8192),  
                        reddit VARCHAR(8192),  
                        start_date DATE,
                        end_date DATE,
                        is_current INTEGER
                    );
                    """
                )
            )
            print("Table 'crypto_description' created successfully.")
        else:
            print("Table 'crypto_description' already exists.")

        # Create dim_date if it does not exist
        if not table_exists("dim_date"):
            connection.execute(
                text(
                    """
                    CREATE TABLE "2024_tomas_ignacio_latorre_schema".dim_date (
                        date DATE NOT NULL PRIMARY KEY,  
                        year INT NOT NULL,               
                        month INT NOT NULL,              
                        week_number INT NOT NULL,        
                        day INT NOT NULL,                
                        yearmonth VARCHAR(6) NOT NULL,   
                        month_name VARCHAR(20) NOT NULL, 
                        day_of_week INT NOT NULL,        
                        day_of_year INT NOT NULL,        
                        week_of_year INT NOT NULL,       
                        quarter INT NOT NULL,            
                        semester INT NOT NULL,           
                        is_weekend BOOLEAN NOT NULL      
                    );
                    """
                )
            )
            print("Table 'dim_date' created successfully.")
        else:
            print("Table 'dim_date' already exists.")

        # Create daily_crypto_prices table if it does not exist
        if not table_exists("daily_crypto_prices"):
            connection.execute(
                text(
                    """
                    CREATE TABLE "2024_tomas_ignacio_latorre_schema".daily_crypto_prices (
                        id_record BIGINT IDENTITY(1,1) PRIMARY KEY,
                        date DATE NOT NULL,                
                        time TIME NOT NULL,                
                        symbol VARCHAR(10) NOT NULL, 
                        open_price DECIMAL(18, 8),         
                        high_price DECIMAL(18, 8),         
                        low_price DECIMAL(18, 8),          
                        close_price DECIMAL(18, 8),        
                        FOREIGN KEY (symbol) REFERENCES "2024_tomas_ignacio_latorre_schema".crypto_description(symbol),
                        FOREIGN KEY (date) REFERENCES "2024_tomas_ignacio_latorre_schema".dim_date(date)
                    );
                    """
                )
            )
            print("Table 'daily_crypto_prices' created successfully.")
        else:
            print("Table 'daily_crypto_prices' already exists.")

        # Create crypto_volatility_and_performance table if it does not exist
        if not table_exists("crypto_volatility_and_performance"):
            connection.execute(
                text(
                    """
                    CREATE TABLE "2024_tomas_ignacio_latorre_schema".crypto_volatility_and_performance (
                        id_record BIGINT IDENTITY(1,1) PRIMARY KEY,
                        date DATE NOT NULL,                
                        symbol VARCHAR(10) NOT NULL, 
                        category VARCHAR(50),  
                        time_interval VARCHAR(255),  
                        low_price DECIMAL(18, 8),         
                        high_price DECIMAL(18, 8),         
                        volatility DECIMAL(18, 8),         
                        open_price DECIMAL(18, 8),         
                        close_price DECIMAL(18, 8),        
                        return DECIMAL(18, 8),     
                        range DECIMAL(18, 8),     
                        average_price DECIMAL(18, 8),  
                        standard_desviation DECIMAL(18, 8), 

                        FOREIGN KEY (symbol) REFERENCES "2024_tomas_ignacio_latorre_schema".crypto_description(symbol),
                        FOREIGN KEY (date) REFERENCES "2024_tomas_ignacio_latorre_schema".dim_date(date)
                    );
                    """
                )
            )
            print("Table 'crypto_volatility_and_performance' created successfully.")
        else:
            print("Table 'crypto_volatility_and_performance' already exists.")
