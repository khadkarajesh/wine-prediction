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


@dag(dag_id='data-validator-task-flow',
     default_args=default_args,
     description="Validates data",
     schedule_interval='*/2 * * * *',
     start_date=days_ago(2),
     tags=['data-validator-task-flow'])
def validation_task():
    @task()
    def validate_data_with_great_expectations():
        # context = ge.data_context.DataContext(str(GE_ROOT_PATH))
        # batch_kwargs_file = {
        #     'path': str(Path.cwd()) + '/data/validation_data.csv',
        #     'datasource': 'wine_datasource'
        # }
        # batch_file = context.get_batch(batch_kwargs_file, "wine_suite")
        # results = context.run_validation_operator(assets_to_validate=[batch_file])
        # if not results["success"]:
        #     raise AirflowException("Validation of the data is not successful")
        # else:
        #     logging.info("oho success we found")

        context = ge.data_context.DataContext(str(GE_ROOT_PATH))
        batch_request = {
            'datasource_name': 'wine_datasource',
            'data_connector_name': 'default_inferred_data_connector_name',
            'data_asset_name': 'validation_data.csv'
        }
        expectation_suite_name = "wine_suite"
        validator = context.get_validator(batch_request=BatchRequest(**batch_request),
                                          expectation_suite_name=expectation_suite_name)
        # validation_result = validator.validate_expectation(expectation_suite_name)
        result = validator.validate(expectation_suite=expectation_suite_name, only_return_failures=True,
                                    data_context=context)
        if result:
            logging.info(f"failed the data pipeline {result}")
        else:
            logging.info(f"succeed the validation pipeline")
        # validation_result = validator.validate(expectation_suite=expectation_suite_name)
        # logging.info(f"lets check validation result {validation_result}")
        # checkpoint_config = {
        #     "class_name": "SimpleCheckpoint",
        #     "validations": [
        #         {
        #             "batch_request": batch_request,
        #             "expectation_suite_name": expectation_suite_name
        #         }
        #     ]
        # }
        #
        # checkpoint = SimpleCheckpoint(
        #     f"_tmp_checkpoint_{expectation_suite_name}",
        #     context,
        #     **checkpoint_config
        # )
        # checkpoint_result = checkpoint.run()
        # if checkpoint_result.success:
        #     logging.info("bam success the operation")
        # else:
        #     logging.info("bam failed operation")

    validate_data_with_great_expectations()


dag = validation_task()
