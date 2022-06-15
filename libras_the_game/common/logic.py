# Python imports
from http.client import INTERNAL_SERVER_ERROR

# Internal imports
from libras_the_game.common.errors.base_error import BaseError
from libras_the_game.common.errors.field_error import FieldError
from libras_the_game.common.models.error_response import ErrorResponse


def build_error_response(exception: BaseError):
    if isinstance(exception, BaseError) and len(exception.field_errors):
        status_code = exception.code
        field_errors = exception.field_errors
    else:
        status_code = INTERNAL_SERVER_ERROR
        field_errors = [
            FieldError(field=str(exception.__class__), message=str(exception))
        ]
    return ErrorResponse(status_code=status_code, errors=field_errors)
