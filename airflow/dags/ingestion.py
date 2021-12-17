import json
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pathlib import Path
import great_expectations as ge
import pandas as pd
import requests
from airflow import AirflowException
from airflow.models import Variable
from airflow.models.dag import dag
from airflow.operators.python import task
from airflow.utils.dates import days_ago
from requests import Response

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

MOCK_FILE_NAME = "validation_data.csv"
DRIFT_FILE_NAME = "validation_data_drift.csv"

GE_ROOT_PATH = Path.cwd() / 'great_expectations'
DATA_ROOT_PATH = Path.cwd() / 'airflow/data'
DATA_INPUT_PATH = DATA_ROOT_PATH / 'input'
DATA_OUTPUT_PATH = DATA_ROOT_PATH / 'output'
PRODUCTION_DATA_INPUT_FILE = DATA_INPUT_PATH / 'wine.csv'
PRODUCTION_DATA_OUTPUT_FILE = DATA_OUTPUT_PATH / MOCK_FILE_NAME
PRODUCTION_DATA_DRIFT_OUTPUT_FILE = DATA_OUTPUT_PATH / DRIFT_FILE_NAME

DRIFT_MIN = 1.0
DRIFT_MAX = 2.0
MIN = 6.0
MAX = 20.0

DATA_PATH = Path.cwd() / "airflow/data"
BASE_URL = "http://127.0.0.1:5000/api/v1"

NOTIFICATION_MESSAGE = "There is drift in data. please take corrective action ahead"


@dag(dag_id='data_ingestion_pipeline',
     default_args=default_args,
     description="Data Ingestion Pipeline",
     schedule_interval='*/5 * * * *',
     start_date=days_ago(2),
     tags=['data_ingestion_pipeline'])
def ingestion_pipeline():
    @task()
    def generate():
        df = pd.read_csv(PRODUCTION_DATA_INPUT_FILE)
        df_copy = df.copy()
        df_copy.drop('label', inplace=True, axis=1)
        random_row = df_copy.sample(n=10)
        return random_row

    @task()
    def store(dataFrame: pd.DataFrame):
        dataFrame.to_csv(PRODUCTION_DATA_OUTPUT_FILE, index=False)
        return str(PRODUCTION_DATA_OUTPUT_FILE)

    def is_drift():
        return Variable.get("drift") == 'true'

    def get_max_value():
        return DRIFT_MAX if is_drift() else MAX

    def get_min_value():
        return DRIFT_MIN if is_drift() else MIN

    @task()
    def validate(file_name: str):
        data_frame = pd.read_csv(PRODUCTION_DATA_DRIFT_OUTPUT_FILE if is_drift() else file_name)
        ge_df = ge.from_pandas(data_frame)

        ge_df.expect_column_values_to_not_be_null(column="fixed acidity")
        result = ge_df.expect_column_values_to_be_between(
            column="fixed acidity",
            min_value=get_min_value(),
            max_value=get_max_value(),
            strict_max=True,
            strict_min=True
        )

        # if not result['success']:
        #     send_email()
        #     raise AirflowException("Data drift detected")
        return data_frame.to_numpy().tolist()

    def send_email():
        port = Variable.get("mail_port")
        password = Variable.get("mail_password")

        sender_email = Variable.get("sender_email")
        receiver_email = Variable.get("receiver_email")

        message = MIMEMultipart("alternative")
        message["Subject"] = "Data Drift Detected"
        message['From'] = sender_email
        message['To'] = receiver_email

        email_body = MIMEText(NOTIFICATION_MESSAGE, "plain")
        message.attach(email_body)

        context = ssl.create_default_context()
        with smtplib.SMTP(Variable.get("smtp"), port) as server:
            try:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                logging.info(f"exception while sending email {e}")

    @task()
    def predict(batch_data):
        response: Response = requests.post(BASE_URL + "/batch-predictions", json=json.dumps(batch_data))
        if response.status_code == 200:
            response_body = response.json()
            logging.info(f"predicated successfully {response_body}")

    random_data = generate()
    file = store(random_data)
    records = validate(file)
    predict(records)


dag = ingestion_pipeline()
