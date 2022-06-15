# Pip imports
from flask import Blueprint
from flask_restful import Api


game_bp = Blueprint("game", __name__, url_prefix="/game")
game_api = Api(game_bp)

from . import routes
