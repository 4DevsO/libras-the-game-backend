# Pip imports
from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    username: str
    password: str
    database: str
    cluster: str

    @property
    def database_uri(self):
        host = f"{self.username}:{self.password}@{self.cluster}/{self.database}"
        return f"mongodb+srv://{host}?retryWrites=true&w=majority"
