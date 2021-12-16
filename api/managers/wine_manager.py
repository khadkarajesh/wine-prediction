from pathlib import Path

import joblib
import pandas as pd

from api.common import db
from api.ml import COLUMN_TRANSFORMER, MODEL, LABEL_ENCODER
from api.models.unprocessed_wine import UnprocessedWine
from api.models.wine import Wine

MODEL_DIR = Path.cwd() / Path('api/ml/models')
COLUMNS = ["fixed acidity",
           "volatile acidity",
           "citric acid",
           "residual sugar",
           "chlorides",
           "free sulfur dioxide",
           "total sulfur dioxide",
           "density",
           "pH",
           "sulphates",
           "alcohol",
           "quality"]


def save_prediction(wine: Wine):
    df = pd.DataFrame(columns=COLUMNS, data=[wine.to_array()])
    column_transformer = joblib.load(MODEL_DIR / COLUMN_TRANSFORMER)
    df = column_transformer.fit_transform(df)

    model = joblib.load(MODEL_DIR / MODEL)
    encoder = joblib.load(MODEL_DIR / LABEL_ENCODER)

    wine.predicted_label = encoder.inverse_transform(model.predict(df))[0]
    db.session.add(wine)
    db.session.commit()


def save_unprocessed_data(bulk_data):
    batch_records = []
    for record in bulk_data:
        wine = UnprocessedWine.to_obj(record)
        batch_records.append(wine)
    db.session.add_all(batch_records)
    db.session.commit()


def save_batch_prediction(bulk_data):
    df = pd.DataFrame(columns=COLUMNS, data=bulk_data)
    column_transformer = joblib.load(MODEL_DIR / COLUMN_TRANSFORMER)
    df = column_transformer.fit_transform(df)

    model = joblib.load(MODEL_DIR / MODEL)
    encoder = joblib.load(MODEL_DIR / LABEL_ENCODER)
    batch_records = []
    for record in bulk_data:
        wine = Wine.to_obj(record)
        wine.predicted_label = encoder.inverse_transform(model.predict(df))[0]
        batch_records.append(wine)
    db.session.add_all(batch_records)
    db.session.commit()


def get_predictions():
    return Wine.query.all()
