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
1. Navigate to root of the project
2. Set environment variables
   ```bash
   export FLASK_APP=app:create_app
   export APP_SETTINGS="api.config.DevelopmentConfig"
   ```
3. Run Flask
   ```bash
   flask run
   ```

### Run Frontend
1. Navigate to the ```frontend``` directory of application
2. Run streamlit application as:
```bash
   streamlit run run.py
```

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
5. Start Airflow Scheduler
   ```bash
   # Set Environment variable to use postgresql as database to store airflow log
   export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow_user:airflow_pass@localhost/wine_airflow
   
   airflow scheduler
   ```
6. Start Web Server
   ```bash
   # Set Environment variable to use postgresql as database to store airflow log
   export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow_user:airflow_pass@localhost/wine_airflow
   
   airflow webserver
   ```
Once you run the webserver you can accesss airflow dashboard on ```http://localhost:8080```.

Airflow has following data ingestion pipeline:

![airflow_diagram](/media/airflow.png)

When the data validation fails, airflow sends email to the respective member which can be configured by adding following variables in airflow. To check this scenario we can enable ```mimic_validation_fail``` in airflow variable.

![airflow_diagram](/media/airflow_variable.png)

   

