import requests
import streamlit as st
import pandas as pd
from requests import Response

BASE_URL = "http://127.0.0.1:5000/api/v1"

HOME_MENU = "Home"
PREDICT_MENU = "Predict"


def display_data():
    response = requests.get(BASE_URL + "/predictions")
    if response.status_code == 200:
        response_body = response.json()
        df = pd.DataFrame(response_body)
        table_df = df.copy()
        table_df.drop(['id', 'created_at'], inplace=True, axis=1)
        st.table(table_df)


def show_form():
    global form, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, quality
    form = st.form(key='my_form')
    fixed_acidity = form.text_input(label='fixed acidity')
    volatile_acidity = form.text_input(label='volatile acidity')
    citric_acid = form.text_input(label='citric acid')
    residual_sugar = form.text_input(label='residual sugar')
    chlorides = form.text_input(label='chlorides')
    free_sulfur_dioxide = form.text_input(label='free sulfur dioxide')
    total_sulfur_dioxide = form.text_input(label='total sulfur dioxide')
    density = form.text_input(label='density')
    ph = form.text_input(label='pH')
    sulphates = form.text_input(label='sulphates')
    alcohol = form.text_input(label='alcohol')
    quality = form.text_input(label='quality')
    st.session_state['page'] = "Predict"

    submit_button = form.form_submit_button(label='Check')

    if submit_button:
        body = {
            'fixed_acidity': fixed_acidity,
            'volatile_acidity': volatile_acidity,
            'citric_acid': citric_acid,
            'residual_sugar': residual_sugar,
            'chlorides': chlorides,
            'free_sulfur_dioxide': free_sulfur_dioxide,
            'total_sulfur_dioxide': total_sulfur_dioxide,
            'density': density,
            'ph': ph,
            'sulphates': sulphates,
            'alcohol': alcohol,
            'quality': quality
        }
        response: Response = requests.post(BASE_URL + "/predictions", json=body)
        if response.status_code == 200:
            response_body = response.json()
            st.write(f"Wine label is :{response_body['predicted_label']}")
        else:
            st.write(f"Couldn't predict wine label")


if 'page' not in st.session_state:
    st.session_state['page'] = HOME_MENU
if st.session_state['page'] == HOME_MENU:
    display_data()

if st.session_state['page'] == PREDICT_MENU:
    show_form()


def change_menu(v):
    print(v, v not in st.session_state['page'])
    if v not in st.session_state['page']:
        st.session_state['page'] = v


st.sidebar.button('Home', on_click=change_menu, args=(HOME_MENU,))
st.sidebar.button('Predict', on_click=change_menu, args=(PREDICT_MENU,))
