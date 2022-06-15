# Pip imports
from pydantic import HttpUrl

# Internal imports
from libras_the_game.common.models.py_base_model import PyBaseModel


class HandConfig(PyBaseModel):
    name: str
    image: HttpUrl
