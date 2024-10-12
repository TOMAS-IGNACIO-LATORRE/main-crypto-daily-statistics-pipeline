import os
from datetime import datetime
from typing import Any, Dict, Optional
from airflow.utils.email import send_email
from dotenv import load_dotenv  # Importa dotenv para cargar variables de entorno

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el email desde el archivo .env
ALERT_EMAIL = os.getenv("ALERT_EMAIL")  # Fallback por si no se encuentra la variable



def send_status_email(success: bool = True, context: Optional[Dict[str, Any]] = None) -> None:
    """Sends an email notification indicating the success or failure of the ETL process.

    This function sends an email notification based on the status of the ETL process. If the ETL
    process failed, the email will include error information extracted from the context provided
    by Airflow.

    Args:
        success (bool): Indicates whether the ETL process was successful or not. Defaults to True.
        context (Optional[Dict[str, Any]]): Airflow context dictionary containing task and DAG info.
            If not provided and `success` is False, the email will have limited information.

    Returns:
        None: This function does not return any value.
    """
    current_timestamp_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if success:
        subject = f"✅main-crypto-daily-statistics-pipeline: Corrida Exitosa"
        body = f"""
        <p>El proceso ETL para main-crypto-daily-statistics-pipeline se ha completado exitosamente en el siguiente horario: {current_timestamp_at}.</p>
        <p>No se requieren más acciones.</p>
        """
    else:
        subject = f"❌ main-crypto-daily-statistics-pipeline: Errores en la corrida"

        dag_id = context["dag"].dag_id if context and context.get("dag") else "Desconocido"
        task_id = (
            context["task_instance"].task_id
            if context and context.get("task_instance")
            else "Desconocido"
        )
        execution_date = (
            context["execution_date"].strftime("%Y-%m-%d %H:%M:%S")
            if context and context.get("execution_date")
            else current_timestamp_at
        )
        log_url = (
            context["task_instance"].log_url
            if context and context.get("task_instance")
            else "No disponible"
        )
        error = (
            context.get("exception", "No hay mensajes de error disponibles.")
            if context
            else "No hay mensajes de error disponibles."
        )

        body = f"""
        <p>El proceso ETL ha fallado. Mira los detalles más abajo:</p>
        <p><b>Dag:</b> {dag_id}</p>
        <p><b>Task:</b> {task_id}</p>
        <p><b>Fecha de ejecución:</b> {execution_date}</p>
        <p><b>Error:</b> {error}</p>
        <p>Para más detalles, por favor acceda al siguiente link: <a href="{log_url}">logs</a>.</p>
        """

    send_email(ALERT_EMAIL, subject, body)


def on_failure_callback(context: Dict[str, Any]) -> None:
    """Callback function to be executed on task failure.

    This function is intended to be used as a callback in Airflow tasks. It sends an email with
    error information extracted from the provided context when the task fails.

    Args:
        context (Dict[str, Any]): Airflow context dictionary containing task and DAG info. This
            context is used to extract information about the failed task and include it in the
            failure notification email.

    Returns:
        None: This function does not return any value.
    """
    send_status_email(success=False, context=context)
