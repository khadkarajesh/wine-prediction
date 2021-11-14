from flask import Blueprint
from flask_restful import Api

from api.resources.prediction import PredictionResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)
api.add_resource(PredictionResource, '/predictions')
