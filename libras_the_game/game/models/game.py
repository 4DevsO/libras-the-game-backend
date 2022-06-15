# Python imports
from typing import List

# Pip imports
from bson import ObjectId
from pydantic import BaseModel

# Internal imports
from libras_the_game.hand_configs.models import HandConfig


class Game(BaseModel):
    words: List[str]
    hand_config: HandConfig
    answer: str

    class Config:
        json_encoders = {ObjectId: str}
