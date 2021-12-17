import json

from flask_restful import Resource
from flask import request

from api.managers.wine_manager import save_batch_prediction


class BatchPredictionResource(Resource):
    @classmethod
    def post(cls):
        bulk_records = request.get_json()
        save_batch_prediction(json.loads(bulk_records))
        return {
            "success": True
        }
