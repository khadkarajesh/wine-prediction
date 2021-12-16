import json
import logging
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.models.dag import dag
from airflow.operators.python import PythonOperator, task
from airflow.utils.dates import days_ago
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.core.batch import BatchRequest
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from requests import Response
import requests

from airflow import AirflowException
import great_expectations as ge

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

# dag = DAG(dag_id='data-validator',
#           default_args=default_args,
#           description="Validates data",
#           schedule_interval='*/2 * * * *',
#           start_date=days_ago(2),
#           tags=['data-validator'])

GE_ROOT_PATH = Path.cwd() / 'great_expectations'
DATA_ROOT_PATH = Path.cwd() / 'airflow/data/output'
PRODUCTION_DATA = DATA_ROOT_PATH / 'validation_data.csv'
BASE_URL = "http://127.0.0.1:5000/api/v1"


# def notify_on_data_drift_detection(checkpoint: CheckpointResult):
#     if not checkpoint.success:
#         logging.info("send email")
#
#
# def predict(path):
#     logging.info("reached here")
#     import requests
#     df = pd.read_csv(Path(path))
#     records = df.to_numpy().tolist()
#     response: Response = requests.post(BASE_URL + "/batch-predictions", json=records)
#     if response.status_code == 200:
#         response_body = response.json()
#         logging.info(f"response ::{response_body}")
#     else:
#         logging.info(f"response ::{response}")
#
#
# validate_data = GreatExpectationsOperator(
#     task_id='validate_source_data',
#     assets_to_validate=[
#         {
#             'batch_kwargs': {
#                 'path': str(Path.cwd()) + '/data/validation_data.csv',
#                 'datasource': 'wine_datasource'
#             },
#             'expectation_suite_name': 'wine_suite'
#         }
#     ],
#     data_context_root_dir=str(GE_ROOT_PATH),
#     dag=dag,
#     validation_failure_callback=notify_on_data_drift_detection
# )
#
#
# def display_result():
#     logging.info("Show result, I am at the end")
#
#
# make_inference = PythonOperator(task_id="make_inference",
#                                 python_callable=predict,
#                                 dag=dag,
#                                 op_kwargs={"path": str(PRODUCTION_DATA)})
#
# display_success = PythonOperator(task_id="display_result",
#                                  python_callable=display_result,
#                                  dag=dag)
#
# validate_data >> make_inference >> display_success


# @dag(dag_id='data-validator',
#      default_args=default_args,
#      description="Validates data",
#      schedule_interval='*/2 * * * *',
#      start_date=days_ago(2),
#      tags=['data-validator'])
# def validate_data():
#     # @task()
#     # def check_data_quality():
#     #     GreatExpectationsOperator(
#     #         task_id='validate_source_data',
#     #         assets_to_validate=[
#     #             {
#     #                 'batch_kwargs': {
#     #                     'path': str(Path.cwd()) + '/data/validation_data.csv',
#     #                     'datasource': 'wine_datasource'
#     #                 },
#     #                 'expectation_suite_name': 'wine_suite'
#     #             }
#     #         ],
#     #         data_context_root_dir=str(GE_ROOT_PATH),
#     #         validation_failure_callback=notify_on_data_drift_detection
#     #     )
#
#     @task()
#     def predict(path):
#         logging.info("reached here")
#         import requests
#         df = pd.read_csv(Path(path))
#         records = df.to_numpy().tolist()
#         response: Response = requests.post(BASE_URL + "/batch-predictions", json=records)
#         if response.status_code == 200:
#             response_body = response.json()
#             logging.info(f"response ::{response_body}")
#         else:
#             logging.info(f"response ::{response}")
#
#     GreatExpectationsOperator(
#         task_id='validate_source_data',
#         assets_to_validate=[
#             {
#                 'batch_kwargs': {
#                     'path': str(Path.cwd()) + '/data/validation_data.csv',
#                     'datasource': 'wine_datasource'
#                 },
#                 'expectation_suite_name': 'wine_suite'
#             }
#         ],
#         data_context_root_dir=str(GE_ROOT_PATH),
#         validation_failure_callback=notify_on_data_drift_detection
#     )
#     predict(str(PRODUCTION_DATA))
#
#
# dag = validate_data()


@dag(dag_id='data-validator-task-flow-test-1',
     default_args=default_args,
     description="Validates data",
     schedule_interval='*/2 * * * *',
     start_date=days_ago(2),
     tags=['data-validator-task-flow'])
def validation_task():
    @task()
    def validate_data_with_great_expectations():
        data_frame = pd.read_csv(str(PRODUCTION_DATA))
        ge_df = ge.from_pandas(data_frame)
        result = ge_df.expect_column_values_to_be_between(
            column="fixed acidity",
            min_value=1,
            max_value=2,
            strict_min=True,
            strict_max=True,
            catch_exceptions=True
        )
        if not result['success']:
            logging.info("could not validate schema")
            raise AirflowException("Invalid Schema")
        else:
            logging.info("validated schema")
        return data_frame.to_numpy().tolist()

    @task()
    def predict(batch_data):
        logging.info("reached here")
        response: Response = requests.post(BASE_URL + "/batch-predictions", json=json.dumps(batch_data))
        if response.status_code == 200:
            response_body = response.json()
            logging.info(f"response ::{response_body}")
        else:
            logging.info(f"response ::{response}")

    records = validate_data_with_great_expectations()
    predict(records)


dag = validation_task()