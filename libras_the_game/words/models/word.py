# Python imports
from typing import List

# Pip imports
from pydantic import Field
from pydantic_mongo import ObjectIdField

# Internal imports
from libras_the_game.common.models.py_base_model import PyBaseModel
from libras_the_game.hand_configs.models.hand_config import HandConfig


class Word(PyBaseModel):
    word: str
    hand_configs: List[ObjectIdField]
    hand_configs_obj: List[HandConfig] = Field(default=None, exclude=True)
