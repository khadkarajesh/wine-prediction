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
   i) creaate database in posgresSQL
   ii) create .env in the project schemas directory to provide postgresSQL db name, user, password and db port.
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
