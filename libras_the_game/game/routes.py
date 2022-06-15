# Pip imports
from flask_restful import Resource

# Internal imports
from libras_the_game.common.decorators.use_pydantic import use_pydantic
from libras_the_game.game.services import get_game

from . import game_api


class Games(Resource):
    @use_pydantic()
    def get(self):
        return get_game()


game_api.add_resource(Games, "")
