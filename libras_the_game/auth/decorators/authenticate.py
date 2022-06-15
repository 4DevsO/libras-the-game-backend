# Python imports
from functools import wraps
from typing import Callable

# Pip imports
from flask import g, request

# Internal imports
from libras_the_game.auth.service import validate_auth_token
from libras_the_game.common.errors import InvalidCredentialsError


def authenticate(func: Callable):
    @wraps(func)
    def decorate(*args, **kwargs) -> Callable:
        bearer_token = request.headers.get("Authorization", None)
        if not bearer_token:
            raise InvalidCredentialsError("Authentication token is missing")

        user = validate_auth_token(bearer_token)
        g.user = user

        return func(*args, **kwargs)

    return decorate
