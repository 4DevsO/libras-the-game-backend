# Pip imports
from flask import Flask
from flask_cors import CORS

# Internal imports
from libras_the_game.common.clients.imgur_client import ImgurClient
from libras_the_game.config.settings import Settings
from libras_the_game.database import Database
from libras_the_game.error_handler import ErrorHandler
from libras_the_game.game import game_bp
from libras_the_game.hand_configs import hand_configs_bp
from libras_the_game.words import words_bp


def create_app(is_production: bool = False) -> Flask:
    settings_file = "settings.dev.json"
    if is_production:
        settings_file = "settings.json"
    settings = Settings.parse_file(f"libras_the_game/config/{settings_file}")

    app = Flask(__name__)
    CORS(app)

    app.config["settings"] = settings

    Database.init_app(app)
    ImgurClient.init_app(app)
    ErrorHandler.init_app(app)

    app.register_blueprint(hand_configs_bp)
    app.register_blueprint(words_bp)
    app.register_blueprint(game_bp)

    return app
