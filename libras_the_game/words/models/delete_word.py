# Pip imports
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class DeleteWord(BaseModel):
    id: ObjectIdField = None
    word: str = None

    class Config:
        json_encoders = {ObjectIdField: str}
