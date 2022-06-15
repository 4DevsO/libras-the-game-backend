# Python imports
from http.client import BAD_REQUEST
from typing import Union

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError


class ResourceNotFoundError(BaseError):
    code = BAD_REQUEST

    def __init__(self, resources: dict[str, Union[str, None]]) -> None:
        errors = []
        for field, value in resources.items():
            if value:
                message = f"Resource {value} not found"
            else:
                message = "Resource not found"
            errors.append(FieldError(field=field, message=message))
        super().__init__(field_errors=errors)
