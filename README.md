# wine-prediction
Wine prediction classifies the whether the wine is white or red based upon the parameters like: acidity, sugar etc.

## Architecture Diagram
------

![dsp *architecture*]

[dsp *architecture*]: architecture.jpg "project architecture"
## Used Technologies
------
* Flask
* Python
* Streamlit
* Postgresql
* AirFlow 2.2
* Grafana

## Steps to Run Application
1. Create a virtual environment with python3
```shell
python3 -m venv wine_prediction
```
Activate the virtual environment:
```shell
cd wine_prediction
source /bin/activate
```
2. Install dependencies 
```shell
pip install -r requirements.txt
   ```
2. Setup Script path and environmental variables
```shell
~/wine-prediction/api/app.py

FLASK_ENV=development;
APP_SETTINGS=config.DevelopmentConfig
```
3. Run API
```shell
flask run app.py
```
Once we run the webserver you can access server in
http://127.0.0.1:5000/
4. Run Frontend in another terminal
```shell
# To view the frontend application & emulate the server run
streamlit run run.py
```
We can view the frontend application in the following link  
http://127.0.0.1:8501/
5. Run Airflow

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
   

