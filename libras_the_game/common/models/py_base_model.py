# Pip imports
from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class PyBaseModel(BaseModel):
    id: ObjectIdField = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda v: str(v)}
