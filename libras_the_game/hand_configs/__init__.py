# Pip imports
from flask import Blueprint
from flask_restful import Api


hand_configs_bp = Blueprint("hand_configs", __name__, url_prefix="/hand_configs")
hand_configs_api = Api(hand_configs_bp)

from . import routes
