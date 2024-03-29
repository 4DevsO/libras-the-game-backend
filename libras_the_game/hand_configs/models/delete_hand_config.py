# Pip imports
from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class DeleteHandConfig(BaseModel):
    id: ObjectIdField = None
    name: str = None

    class Config:
        json_encoders = {ObjectIdField: str, ObjectId: str}
