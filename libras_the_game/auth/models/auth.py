# Pip imports
from bson import ObjectId
from pydantic import BaseModel


class Auth(BaseModel):
    token: str
    expires_in: str

    class Config:
        json_encoders = {ObjectId: str}
