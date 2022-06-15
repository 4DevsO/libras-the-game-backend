# Python imports
from http.client import INTERNAL_SERVER_ERROR

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError


class InternalServerError(BaseError):
    code = INTERNAL_SERVER_ERROR

    def __init__(self, message: str, field: str = "server"):
        error = FieldError(field=field, message=message)
        super().__init__(field_errors=[error])
