from api.common import db
from api.models import BaseModel


class Wine(BaseModel):
    __tablename__ = 'wines'
    fixed_acidity = db.Column(db.DECIMAL, nullable=False)
    volatile_acidity = db.Column(db.DECIMAL, nullable=False)
    citric_acid = db.Column(db.DECIMAL, nullable=False)
    residual_sugar = db.Column(db.DECIMAL, nullable=False)
    chlorides = db.Column(db.DECIMAL, nullable=False)
    free_sulfur_dioxide = db.Column(db.DECIMAL, nullable=False)
    total_sulfur_dioxide = db.Column(db.DECIMAL, nullable=False)
    density = db.Column(db.DECIMAL, nullable=False)
    ph = db.Column(db.DECIMAL, nullable=False)
    sulphates = db.Column(db.DECIMAL, nullable=False)
    alcohol = db.Column(db.DECIMAL, nullable=False)
    quality = db.Column(db.DECIMAL, nullable=False)
    label = db.Column(db.String, nullable=False)
