from staging.parquet_staging import parquet_create_staging
from typing import Any
from airflow.exceptions import AirflowException
from dotenv import load_dotenv
from variables.config import DIR_PATH, COINS_LIST, coin_id, API_KEY_COINMARKETCAP,DATE_STR

def run_staging(**context: Any) -> None:    
    """
    Executes the staging layer task, which generates parquet files with stock or coin
    data retrieved from external APIs. This function is designed to be executed within an Airflow DAG task, utilizing the 
    context provided by Airflow, such as the execution date, task details, and other 
    dynamic parameters. The function retrieves data, processes it, and stores it in 
    parquet format for further use in downstream tasks.

    Args:
        **context (Any): A dictionary containing execution context information provided
        by Airflow. The `context` can include various parameters such as the execution 
        date (`ds`), task identifier, and other dynamic data relevant to the task.

    Raises:
        AirflowException: If an error occurs during the parquet creation process, this 
        exception is raised to signal task failure in the DAG, allowing Airflow to 
        handle retries, notifications, and other failure-handling mechanisms.
    """
    try:
        parquet_create_staging(context["ds"])
    except AirflowException as e:
        raise e  # Forzar a cancelar a la tarea si se cancela el DAG


if __name__ == "__main__":
    run_staging()