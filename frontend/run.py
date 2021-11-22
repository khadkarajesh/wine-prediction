import requests
import streamlit as st
from requests import Response

"""
# Wine Prediction
"""

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

submit_button = form.form_submit_button(label='Check')

BASE_URL = "http://127.0.0.1:5000/api/v1"

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
