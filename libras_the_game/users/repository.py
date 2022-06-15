# Pip imports
from pydantic_mongo import AbstractRepository

# Internal imports
from libras_the_game.database import Database
from libras_the_game.users.models import User


class UsersRepository(AbstractRepository[User]):
    def __init__(self):
        super().__init__(Database.get_db_client())

    class Meta:
        collection_name = "users"
