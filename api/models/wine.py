from api.common import db
from api.models import BaseModel


class Wine(BaseModel):
    __tablename__ = 'wines'
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
    label = db.Column(db.String, nullable=False)
