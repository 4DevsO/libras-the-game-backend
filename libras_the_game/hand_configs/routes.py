# Pip imports
from flask import request
from flask_restful import Resource

# Internal imports
from libras_the_game.auth.decorators.authenticate import authenticate
from libras_the_game.common.decorators.use_pydantic import use_pydantic
from libras_the_game.hand_configs.models import CreateHandConfig, DeleteHandConfig
from libras_the_game.hand_configs.services import (
    create_hand_config,
    delete_hand_config,
    get_hand_configs,
)

from . import hand_configs_api


class HandConfigs(Resource):
    @use_pydantic(response_many=True)
    def get(self):
        return get_hand_configs()

    @authenticate
    @use_pydantic()
    def post(self, form: CreateHandConfig):
        form.image = request.files["image"].read()
        return create_hand_config(form), 201

    @authenticate
    @use_pydantic()
    def delete(self, query: DeleteHandConfig):
        return delete_hand_config(query)


hand_configs_api.add_resource(HandConfigs, "")
