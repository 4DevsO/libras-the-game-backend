# Python imports
from http.client import CONFLICT
from typing import Union

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError


class DuplicatedResourceError(BaseError):
    def __init__(self, resources: dict[str, Union[str, None]]) -> None:
        errors = []
        for field, value in resources.items():
            if value:
                message = f"Resource {value} already exists"
            else:
                message = "Resource already exists"
            errors.append(FieldError(field=field, message=message))
        super().__init__(code=CONFLICT, field_errors=errors)
