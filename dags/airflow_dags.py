import os
import sys
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tasks.run_staging import run_staging 
from tasks.run_silver import run_silver  
from tasks.run_gold import run_gold  
from tasks.alert_email import send_status_email, on_failure_callback

# Default arguments for the DAG
default_args = {
    "owner": "tomaslatorre",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=7),
    "on_failure_callback": on_failure_callback, # on_failure_callback es una tarea de Airflow que define una función que se llame automáticamente cuando la tarea falla
}

# Define the DAG
with DAG(
    dag_id="crypto_price_dags",
    default_args=default_args,
    description="ETL pipeline to extract, process and transform crypto price data and load it into Redshift Database",
    schedule_interval="0 0 * * *",  # Todos los días a las 4 am UTC
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task to extract data from the API and generate Parquet files (Staging layer)
    staging_task = PythonOperator(
        task_id="staging_run",
        python_callable=run_staging,
        provide_context=True,
    )

    # Task to load Parquet files into Redshift (Silver layer)
    silver_task = PythonOperator(
        task_id="silver_run",
        python_callable=run_silver,
        provide_context=True,
    )

    # Task to create the final attributes table (Gold layer)
    gold_task = PythonOperator(
        task_id="gold_run",
        python_callable=run_gold,
        provide_context=True,
    )

    # Task to send a success email
    email_task = PythonOperator(
        task_id="send_email",
        python_callable=send_status_email,
        op_kwargs={"success": True},  # Correo de éxito se envie igual
    )
    
    # Define task execution sequence
    staging_task >> silver_task >> gold_task >> email_task
