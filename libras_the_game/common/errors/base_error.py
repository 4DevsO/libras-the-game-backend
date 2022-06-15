# Python imports
from http.client import INTERNAL_SERVER_ERROR
from typing import List

# Pip imports
from pydantic import Field
from pydantic.dataclasses import dataclass

# Internal imports
from libras_the_game.common.errors.field_error import FieldError


@dataclass
class BaseError(Exception):
    code: int = INTERNAL_SERVER_ERROR
    field_errors: List[FieldError] = Field(default=[])
