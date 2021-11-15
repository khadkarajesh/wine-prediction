from flask_restful import Resource


class PredictionResource(Resource):
    @classmethod
    def get(cls):
        return {"hello": "world"}

    @classmethod
    def post(cls):
        return {"label": "white"}
