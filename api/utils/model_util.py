import joblib


def get_file(file_path):
    return joblib.load(file_path)


def save_file(object_to_save, file_path):
    joblib.dump(object_to_save, file_path)
