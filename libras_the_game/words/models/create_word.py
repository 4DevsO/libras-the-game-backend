# Python imports
from typing import List, Optional

# Pip imports
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class CreateWord(BaseModel):
    word: str
    hand_configs: Optional[List[ObjectIdField]]
    hand_configs_names: Optional[List[str]]
