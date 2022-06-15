# Pip imports
from bson import ObjectId
from pydantic import EmailStr, validator

# Internal imports
from libras_the_game.common.models.py_base_model import PyBaseModel


class User(PyBaseModel):
    email: EmailStr
    password: str

    @validator("id")
    def id_to_str(cls, v):
        return str(v)

    class Config:
        json_encoders = {ObjectId: str}
