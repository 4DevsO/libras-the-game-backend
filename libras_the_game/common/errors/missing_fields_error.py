# Python imports
from http.client import BAD_REQUEST
from typing import List

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError


class MissingFieldsError(BaseError):
    def __init__(self, resources: List[str]) -> None:
        errors = [FieldError(field=r, message="Missing field") for r in resources]
        super().__init__(code=BAD_REQUEST, field_errors=errors)
