import logging
from datetime import timedelta, datetime
from pathlib import Path

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

DATA_PATH = Path.cwd() / "airflow/data"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='mock-data-generator',
     default_args=default_args,
     description="Generate random data",
     schedule_interval='*/1 * * * *',
     start_date=days_ago(2),
     tags=['fake_data_generator']
     )
def generate_data():
    @task()
    def generate_random_data():
        Path.cwd()
        df = pd.read_csv(DATA_PATH / 'input/wine.csv')
        random_row = df.sample(n=10)
        return random_row

    @task()
    def store(dataFrame: pd.DataFrame):
        file_name = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        dataFrame.to_csv(DATA_PATH / f'output/{file_name}.csv', index=False)
        logging.info("created file successfully")

    data = generate_random_data()
    store(data)


dag = generate_data()
