from sqlalchemy.engine import Engine
from variables.connection_redshift import create_redshift_engine
from gold.crypto_volability_and_performance import calculate_crypto_volability_and_performance


def run_gold(**context) -> None:
    """
    Run the gold layer process, which calculates stock attributes
    and inserts the calculated data into the Redshift database.

    Steps:
        1. Create a connection to the Redshift database.
        2. Calculate stock attributes based on daily stock prices for the given date.
        3. Insert the calculated attributes into the relevant table in Redshift.

    Args:
        None

    Raises:
        Exception: If there is an issue with calculating stock attributes
        or the database connection.
    """
    
    conn: Engine = create_redshift_engine()

    # Calculate stock attributes and insert them into Redshift
    calculate_crypto_volability_and_performance(conn, context["ds"])

if __name__ == "__main__":
    run_gold()