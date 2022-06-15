# Pip imports
from pydantic import BaseModel, HttpUrl


class ImgurSettings(BaseModel):
    base_url: HttpUrl
    auth_key: str
