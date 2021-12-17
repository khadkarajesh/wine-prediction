import json

from flask_restful import Resource
from flask import request

from api.managers.wine_manager import save_unprocessed_data


class DataUploadResource(Resource):
    @classmethod
    def post(cls):
        bulk_records = request.get_json()
        save_unprocessed_data(json.loads(bulk_records))
        return {
            "success": True
        }
