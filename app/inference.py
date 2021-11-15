from app import MODEL
from app.preprocess import preprocess, decode_label
from utils.model_util import get_file


def predict(dataframe, model_dir, training=False):
    preprocessed_dataframe = preprocess(dataframe, model_dir) if not training else dataframe
    model = get_file(model_dir / MODEL)
    if training: return model.predict(preprocessed_dataframe)
    return decode_label(model.predict(preprocessed_dataframe), model_dir)
