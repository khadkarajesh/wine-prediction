from flask import request
from flask_restful import Resource

from api.managers.wine_manager import save_prediction, get_predictions
from api.schemas import WineSchema


class PredictionResource(Resource):
    @classmethod
    def get(cls):
        wine_schema = WineSchema(many=True)
        return wine_schema.dump(get_predictions())

    @classmethod
    def post(cls):
        wine_schema = WineSchema()
        wine = wine_schema.load(request.get_json())
        save_prediction(wine)
        return wine_schema.dump(wine)
