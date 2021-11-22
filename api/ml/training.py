from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from api.ml import MODEL
from api.ml.inference import predict
from api.ml.preprocess import encode_label, preprocess
from api.utils.model_util import save_file


def train(training_data_path, model_dir):
    x_train, x_test, y_train, y_test = __get_preprocessed_train_data(model_dir, training_data_path)
    model = LogisticRegression()
    model.fit(x_train, y_train)
    save_file(model, model_dir / MODEL)
    y_predicted = predict(x_test, model_dir, training=True)
    return {'accuracy': accuracy_score(y_test, y_predicted)}


def __get_preprocessed_train_data(model_dir, training_data_filepath):
    dataframe = pd.read_csv(Path(training_data_filepath))
    df = dataframe.copy()
    y = encode_label(df['label'], model_dir)
    x = preprocess(df, model_dir)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=0)
    return x_train, x_test, y_train, y_test
