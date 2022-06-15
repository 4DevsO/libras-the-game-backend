# Python imports
from typing import Optional

# Pip imports
from pydantic import BaseModel


class CreateHandConfig(BaseModel):
    name: str
    image: Optional[bytes]
