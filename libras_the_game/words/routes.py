# Pip imports
from flask_restful import Resource

# Internal imports
from libras_the_game.common.decorators.use_pydantic import use_pydantic
from libras_the_game.common.errors.missing_fields_error import MissingFieldsError
from libras_the_game.words.models import CreateWord, DeleteWord
from libras_the_game.words.services import create_word, delete_word, get_words

from . import words_api


class Words(Resource):
    @use_pydantic(response_many=True)
    def get(self):
        return get_words()

    @use_pydantic()
    def post(self, body: CreateWord):
        if not body.hand_configs and not body.hand_configs_names:
            raise MissingFieldsError(["hand_configs"])
        return create_word(body), 201

    @use_pydantic()
    def delete(self, query: DeleteWord):
        return delete_word(query)


words_api.add_resource(Words, "")
