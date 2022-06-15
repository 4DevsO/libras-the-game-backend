# Pip imports
from flask import Flask, current_app, g
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase


class Database:
    @staticmethod
    def connect() -> MongoClient:
        database_uri: str = current_app.config[
            "settings"
        ].database_settings.database_uri
        return MongoClient(database_uri, serverSelectionTimeoutMS=5000)

    @staticmethod
    def get_db_client() -> MongoDatabase:
        if "db_client" not in g:
            g.db_client = Database.connect()
        database_name: str = current_app.config["settings"].database_settings.database
        return g.db_client[database_name]

    @staticmethod
    def close_db_client(error=None):
        db_client: MongoClient = g.pop("db_client", None)

        if db_client is not None:
            db_client.close()

    @staticmethod
    def init_app(app: Flask):
        app.teardown_appcontext(Database.close_db_client)
