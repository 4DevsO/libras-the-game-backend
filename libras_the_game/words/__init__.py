# Pip imports
from flask import Blueprint
from flask_restful import Api


words_bp = Blueprint("words", __name__, url_prefix="/words")
words_api = Api(words_bp)

from . import routes
