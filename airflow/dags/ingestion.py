from datetime import timedelta, datetime
from airflow.decorators import dag
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='data-validator',
     default_args=default_args,
     description="Validates data",
     schedule_interval='*/1 * * * *',
     start_date=days_ago(2),
     tags=['data-validator'])
def validate_data():
    pass
