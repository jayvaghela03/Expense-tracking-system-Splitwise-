from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
from datetime import datetime, timedelta

default_args = {
    'owner': 'jay',
    'start_date': datetime(2023, 10, 29),  # Set the start date
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'send_report',
    default_args=default_args,
    description='Send an HTTP request weekly',
    schedule_interval=timedelta(weeks=1),  # Run weekly
    catchup=False,
)

def trigger_mail():
    url = "http://0.0.0.0:5000/send-report"  # Include the protocol (e.g., "http://")
    response = requests.get(url)
    print(response.text)  # Print the response content

t1 = PythonOperator(
    task_id='send_slack_notification',
    python_callable=trigger_mail,
    dag=dag)
