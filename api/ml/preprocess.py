from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from api.ml import SCALAR, LABEL_ENCODER, IMPUTER, COLUMN_TRANSFORMER
from api.utils.model_util import get_file, save_file


def preprocess(X: pd.DataFrame, model_dir):
    transformer = _get_column_transformer(model_dir, __get_continuous_columns(X))
    return transformer.fit_transform(X)


def _get_column_transformer(model_dir, features):
    column_transformer_path = model_dir / COLUMN_TRANSFORMER
    if not column_transformer_path.exists():
        transformer = ColumnTransformer(transformers=
                                        [('imputer', get_simple_imputer(model_dir),
                                          features),
                                         ('scalar', get_scalar(model_dir), features)])
        save_file(transformer, column_transformer_path)
    else:
        transformer = get_file(column_transformer_path)
    return transformer


def __get_continuous_columns(dataframe: pd.DataFrame):
    return dataframe.select_dtypes(exclude=[np.object]).columns.tolist()


def get_scalar(model_dir: Path):
    scalar_path = model_dir / SCALAR
    if scalar_path.exists(): return get_file(scalar_path)
    scalar = MinMaxScaler()
    save_file(scalar, scalar_path)
    return scalar


def get_simple_imputer(model_dir: Path):
    imputer_path = model_dir / IMPUTER
    if imputer_path.exists(): return get_file(imputer_path)
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    save_file(imputer, imputer_path)
    return imputer


def get_label_encoder(model_dir: Path):
    label_encoder_path = model_dir / LABEL_ENCODER
    if label_encoder_path.exists(): return get_file(label_encoder_path)
    label_encoder = LabelEncoder()
    return label_encoder


def encode_label(dataframe: pd.DataFrame, model_dir):
    label_encoder_path = model_dir / LABEL_ENCODER
    label_encoder = get_label_encoder(model_dir)
    label_encoder.fit(dataframe)
    save_file(label_encoder, label_encoder_path)
    return label_encoder.transform(dataframe)


def decode_label(data, model_dir):
    label_encoder = get_label_encoder(model_dir)
    return label_encoder.inverse_transform(data)
