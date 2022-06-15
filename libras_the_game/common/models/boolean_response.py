# Pip imports
from pydantic import BaseModel


class BooleanResponse(BaseModel):
    result: bool
