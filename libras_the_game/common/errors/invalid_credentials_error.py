# Python imports
from http.client import UNAUTHORIZED

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError


class InvalidCredentialsError(BaseError):
    def __init__(self, message: str = "email or password incorrect") -> None:
        error = FieldError(field="auth", message=message)
        super().__init__(code=UNAUTHORIZED, field_errors=[error])
