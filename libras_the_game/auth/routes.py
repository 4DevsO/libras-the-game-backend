# Pip imports
from flask_restful import Resource

# Internal imports
from libras_the_game.auth.decorators.authenticate_api import authenticate_api
from libras_the_game.auth.service import sign_in, sign_up
from libras_the_game.common.decorators.use_pydantic import use_pydantic
from libras_the_game.users.models import User

from . import auth_api


class SignIn(Resource):
    @use_pydantic()
    def post(self, body: User):
        return sign_in(body), 201


class SignUp(Resource):
    @authenticate_api
    @use_pydantic()
    def post(self, body: User):
        return sign_up(body)


auth_api.add_resource(SignIn, "/signin")
auth_api.add_resource(SignUp, "/signup")
