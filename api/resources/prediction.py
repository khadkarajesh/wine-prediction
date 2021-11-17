from flask_restful import Resource

from api.models.wine import Wine


class PredictionResource(Resource):
    @classmethod
    def get(cls):
        return {"hello": "world"}

    @classmethod
    def post(cls):
        return {"label": "white"}
