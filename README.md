# wine-prediction
Wine prediction classifies the whether the wine is white or red based upon the parameters like: acidity, sugar etc.

Right now repository consist the following apps:

#### API
- Flask Application which uses the machine learning model to predict the wine type and stores data into the Postgresql. 

#### Frontend
- Streamlit application which provides form to input wine attributes

#### App
- App consists the machine learning pipeline

## Prerequisites 
1. Create virtual environment and activate it
```shell
$ python3 -m venv wine_prediction
```
To activate it:
```shell
cd wine_prediction
source /bin/activate
```

2. Install dependencies 
   ```shell
   pip install -r requirements.txt
   ```
For the necessary dependencies
```shell
sudo apt install libpq-dev python3-dev gcc
```

3. Setup environment variable
   ```shell
   export config=DevelopmentConfig
   ```
4. Create database for postgresSQL
   i) Create database in postgresSQL
   ii) Create .env in the project schemas directory to provide postgresSQL db name, user, password and db port. Example:
   ```shell
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="pgadmin"
   POSTGRES_DB="airflow_db"
   POSTGRES_URL="postgres://${POSTGRES_USR}:${POSTGRES_PWD}@postgres:5432/${POSTGRES_DB}?sslmode=disable"
   ```
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
