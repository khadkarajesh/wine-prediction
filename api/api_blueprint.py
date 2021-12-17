from flask import Blueprint
from flask_restful import Api

from api.resources.batch_prediction import BatchPredictionResource
from api.resources.data_upload import DataUploadResource
from api.resources.prediction import PredictionResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)
api.add_resource(PredictionResource, '/predictions')
api.add_resource(BatchPredictionResource, '/batch-predictions')
api.add_resource(DataUploadResource, '/batch-data-uploads')
