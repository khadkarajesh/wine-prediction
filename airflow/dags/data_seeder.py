import json
import logging
import random
from datetime import timedelta
from pathlib import Path

import pandas as pd
import requests
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from requests import Response

DATA_PATH = Path.cwd() / "airflow/data"
BASE_URL = "http://127.0.0.1:5000/api/v1"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='production_data_seeder',
     default_args=default_args,
     description="Seed production data",
     start_date=days_ago(2),
     tags=['production_data_seeder']
     )
def generate_data():
    @task()
    def read_training_data():
        df = pd.read_csv(DATA_PATH / 'input/wine.csv')
        return df

    @task()
    def store(data_frame: pd.DataFrame):
        batch_data = data_frame.to_numpy().tolist()
        response: Response = requests.post(BASE_URL + "/batch-data-uploads", json=json.dumps(batch_data))
        if response.status_code == 200:
            response_body = response.json()
            logging.info(f"saved data successfully {response_body}")

    data = read_training_data()
    store(data)


dag = generate_data()
