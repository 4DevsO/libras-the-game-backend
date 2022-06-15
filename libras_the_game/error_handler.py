# Pip imports
from flask import Flask, Response

# Internal imports
from libras_the_game.common.logic import build_error_response


class ErrorHandler:
    @staticmethod
    def handle_error(exception: Exception = None) -> Response:
        error_response = build_error_response(exception)
        return error_response.dict(), error_response.status_code

    @staticmethod
    def init_app(app: Flask):
        app.register_error_handler(Exception, ErrorHandler.handle_error)
