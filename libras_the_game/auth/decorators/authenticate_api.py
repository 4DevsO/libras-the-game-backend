# Python imports
from functools import wraps
from typing import Callable

# Pip imports
from flask import request

# Internal imports
from libras_the_game.auth.service import validate_api_key
from libras_the_game.common.errors import InvalidCredentialsError


def authenticate_api(func: Callable):
    @wraps(func)
    def decorate(*args, **kwargs) -> Callable:
        api_key = request.headers.get("X-API-KEY", None)
        if not api_key:
            raise InvalidCredentialsError("X-API-KEY key is missing")

        validate_api_key(api_key)

        return func(*args, **kwargs)

    return decorate
