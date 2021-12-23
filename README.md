# wine-prediction
Wine prediction classifies the whether the wine is white or red based upon the parameters like: acidity, sugar etc.

## Architecture Diagram
------

## Used Technologies
------

## Steps to Run Application
1. Create Virtual Environment and install all requirements stuffs like that
2. [Run API](#run-api)
3. [Run Airflow](#run-airflow)
4. [Run Frontend](#run-frontend)

### Run API

### Run Frontend

### Run Airflow
1. Create database user and grant all permission to that user which will be used to store the logs of airflow
   
   Create user using psql shell. 
   ```psql
   CREATE DATABASE wine_airflow;
   CREATE USER airflow_user WITH ENCRYPTED PASSWORD 'airflow_pass';
   GRANT ALL PRIVILEGES ON DATABASE wine_airflow TO airflow_user;
   ```

2. Go to root directory of project and set env variable ```AIRFLOW_HOME``` as:
   ```bash
   export AIRFLOW_HOME=$PWD/airflow
   ```
3. Initialize database
   ```bash
   airflow db init
   ```
4. Create User (username:admin, password:admin) to access the airflow web application which will be run on ```http://localhost:8080```
   ```bash
   airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@gmail.com --password admin
   ```
5. Set Environment variable to use postgresql as database to store airflow log
   ```bash
   export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow_user:airflow_pass@localhost/wine_airflow
   ```
6. Start Airflow Scheduler
   ```bash
   airflow scheduler
   ```
7. Start Web Server
   ```bash
   airflow webserver
   ```
Once you run the webserver you can accesss airflow dashboard on ```http://localhost:8080```.


Link to the detail section with detail

Right now repository consist the following apps:

#### API
- Flask Application which uses the machine learning model to predict the wine type and stores data into the Postgresql. 

#### Frontend
- Streamlit application which provides form to input wine attributes

#### App
- App consists the machine learning pipeline

## Prerequisites 
1. create virtual environment and activate it
2. Install dependencies 
   ```python
   pip install -r requirements.txt
   ```
3. setup environment variable
   ```shell
   export config=DevelopmentConfig
   ```
4. create database for posgresSQL 
  
   1. creaate database in posgresSQL
   2. create .env in the project schemas directory to provide postgresSQL db name, user, password and db port.
   default posgresSQL user : postgres

### Run Flask API
It needs to run before streamlit, to consume API from frontend. 

   ```python
   flask run app.py
   ```

### Run Frontend application
Then we run the frontend server using cmd given below, now we input the feature and save that predicted label along with the given features in our postgresSQL.

   ```python
   streamlit run run.py
   ```
   

