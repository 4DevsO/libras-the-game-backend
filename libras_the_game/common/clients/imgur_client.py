# Pip imports
from flask import Flask, current_app, g
from pydantic import HttpUrl
from requests import Response, Session

# Internal imports
from libras_the_game.config.imgur_settings import ImgurSettings


class ImgurClient:
    def __init__(self) -> None:
        self.imgur_settings: ImgurSettings = current_app.config[
            "settings"
        ].imgur_settings
        self.client = Session()
        self.client.headers["Authorization"] = self.imgur_settings.auth_key
        self.base_url = self.imgur_settings.base_url

    def upload_image(self, file: bytes) -> HttpUrl:
        payload = {"image": file}
        res: Response = self.client.post(f"{self.base_url}/3/image", data=payload)
        res = res.json()
        return res["data"]["link"]

    @staticmethod
    def get_imgur_client():
        if "imgur_client" not in g:
            g.imgur_client = ImgurClient()
        return g.imgur_client

    @staticmethod
    def close_imgur_client(error=None):
        g.pop("imgur_client", None)

    @staticmethod
    def init_app(app: Flask):
        app.teardown_appcontext(ImgurClient.close_imgur_client)
