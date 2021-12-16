from api.common import db
from api.models import BaseModel


class UnprocessedWine(BaseModel):
    __tablename__ = 'unprocessed_wines'
    fixed_acidity = db.Column(db.Float, nullable=False)
    volatile_acidity = db.Column(db.Float, nullable=False)
    citric_acid = db.Column(db.Float, nullable=False)
    residual_sugar = db.Column(db.Float, nullable=False)
    chlorides = db.Column(db.Float, nullable=False)
    free_sulfur_dioxide = db.Column(db.Float, nullable=False)
    total_sulfur_dioxide = db.Column(db.Float, nullable=False)
    density = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    sulphates = db.Column(db.Float, nullable=False)
    alcohol = db.Column(db.Float, nullable=False)
    quality = db.Column(db.Float, nullable=False)

    @staticmethod
    def to_obj(data):
        wine = UnprocessedWine()
        wine.fixed_acidity = data[0]
        wine.volatile_acidity = data[1]
        wine.citric_acid = data[2]
        wine.residual_sugar = data[3]
        wine.chlorides = data[4]
        wine.free_sulfur_dioxide = data[5]
        wine.total_sulfur_dioxide = data[6]
        wine.density = data[7]
        wine.ph = data[8]
        wine.sulphates = data[9]
        wine.alcohol = data[10]
        wine.quality = data[11]
        return wine
