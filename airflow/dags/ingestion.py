import logging
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(dag_id='data-validator',
          default_args=default_args,
          description="Validates data",
          schedule_interval='*/2 * * * *',
          start_date=days_ago(2),
          tags=['data-validator'])

GE_ROOT_PATH = Path.cwd() / 'great_expectations'
DATA_ROOT_PATH = Path.cwd() / 'data/validation_data.csv'


def notify_on_data_drift_detection(checkpoint: CheckpointResult):
    if not checkpoint.success:
        logging.info(f"--------- sending email to user ------------ checkpoint {checkpoint}")


def validate(path: Path):
    pass


def predict_data():
    pd.read_csv()


validate_data = GreatExpectationsOperator(
    task_id='validate_source_data',
    assets_to_validate=[
        {
            'batch_kwargs': {
                'path': str(DATA_ROOT_PATH),
                'datasource': 'wine_datasource'
            },
            'expectation_suite_name': 'wine_suite'
        }
    ],
    data_context_root_dir=str(GE_ROOT_PATH),
    dag=dag,
    validation_failure_callback=notify_on_data_drift_detection
)

# predict_data = PythonOperator(python_callable=)

validate_data
