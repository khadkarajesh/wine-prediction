from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from app import SCALAR, LABEL_ENCODER
from utils.model_util import get_file, save_file


def preprocess(X: pd.DataFrame, model_dir):
    numerical_features = __get_continuous_columns(X)
    transformer = ColumnTransformer(transformers=
                                    [('imputer', SimpleImputer(missing_values=np.nan, strategy='mean'),
                                      numerical_features),
                                     ('scalar', get_scalar(model_dir), numerical_features)])
    return transformer.fit_transform(X)


def __get_continuous_columns(dataframe: pd.DataFrame):
    return dataframe.select_dtypes(exclude=[np.object]).columns.tolist()


def get_scalar(model_dir: Path):
    scalar_path = model_dir / SCALAR
    if scalar_path.exists(): return get_file(scalar_path)
    scalar = MinMaxScaler()
    save_file(scalar, scalar_path)
    return scalar


def get_label_encoder(model_dir: Path):
    label_encoder_path = model_dir / LABEL_ENCODER
    if label_encoder_path.exists(): return get_file(label_encoder_path)
    label_encoder = LabelEncoder()
    save_file(label_encoder, label_encoder_path)
    return label_encoder


def encode_label(dataframe: pd.DataFrame, model_dir):
    label_encoder = get_label_encoder(model_dir)
    return label_encoder.fit_transform(dataframe)


def decode_label(data, model_dir):
    label_encoder = get_label_encoder(model_dir)
    return label_encoder.inverse_transform(data)
