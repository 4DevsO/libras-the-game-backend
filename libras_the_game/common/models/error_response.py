# Python imports
from typing import List

# Pip imports
from pydantic import BaseModel

# Internal imports
from libras_the_game.common.errors.field_error import FieldError


class ErrorResponse(BaseModel):
    status_code: int
    errors: List[FieldError]
