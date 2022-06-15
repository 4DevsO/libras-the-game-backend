# Python imports
from datetime import datetime, timedelta
from uuid import uuid4

# Pip imports
import jwt
from flask import current_app

# Internal imports
from libras_the_game.auth.models import Auth
from libras_the_game.common.errors import (
    DuplicatedResourceError,
    InvalidCredentialsError,
)
from libras_the_game.config.auth_settings import AuthSettings
from libras_the_game.users.models import User
from libras_the_game.users.service import (
    create_user,
    does_user_exist,
    get_user,
    get_user_by_id,
)


def sign_up(user: User) -> User:
    if does_user_exist(user.email):
        raise DuplicatedResourceError({"user": None})

    created_user = create_user(user)
    created_user.password = ""  # remove password to signup return
    return created_user


def sign_in(user: User) -> Auth:
    auth_settings: AuthSettings = current_app.config["settings"].auth_settings
    logged_user = get_user(user.email, user.password)
    expiration = datetime.utcnow() + timedelta(
        minutes=auth_settings.expiration_time_minutes
    )
    token = jwt.encode(
        {
            "session_id": str(uuid4()),
            "user": {**logged_user.dict()},
            "exp": expiration,
        },
        auth_settings.secret_key,
        "HS256",
    )
    expires_in = int((expiration - datetime.utcnow()).total_seconds())
    return Auth(token=token, expires_in=expires_in)


def validate_auth_token(token: str) -> User:
    try:
        auth_settings: AuthSettings = current_app.config["settings"].auth_settings
        jwt_token = jwt.decode(token, auth_settings.secret_key, ["HS256"])
        return get_user_by_id(jwt_token["user"]["id"])
    except jwt.ExpiredSignatureError:
        raise InvalidCredentialsError("Authentication token is expired")
    except jwt.PyJWTError:
        raise InvalidCredentialsError("Authentication token failed")


def validate_api_key(api_key: str):
    auth_settings: AuthSettings = current_app.config["settings"].auth_settings
    if auth_settings.api_key != api_key:
        raise InvalidCredentialsError("X-API-KEY invalid")
