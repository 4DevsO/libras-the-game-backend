# Pip imports
from pydantic import BaseModel


class AuthSettings(BaseModel):
    api_key: str
    secret_key: str
    expiration_time_minutes: int
