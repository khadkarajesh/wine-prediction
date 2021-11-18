from api.common import db
from api.models.wine import Wine


def save_prediction(wine: Wine):
    db.session.add(wine)
    db.session.commit()


def get_predictions():
    return Wine.query.all()
