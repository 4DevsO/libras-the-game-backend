# Pip imports
from pydantic import BaseModel

# Internal imports
from libras_the_game.config.auth_settings import AuthSettings
from libras_the_game.config.database_settings import DatabaseSettings
from libras_the_game.config.imgur_settings import ImgurSettings


class Settings(BaseModel):
    database_settings: DatabaseSettings
    imgur_settings: ImgurSettings
    auth_settings: AuthSettings
