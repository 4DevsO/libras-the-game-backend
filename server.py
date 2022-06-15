# Python imports
from os import environ

# Internal imports
from libras_the_game.app import create_app


if __name__ == "__main__":
    environment = environ.get("FLASK_ENV", "development")
    is_production = environment == "production"
    port = environ.get("PORT", 3333)

    app = create_app(is_production)
    app.run(debug=not is_production, host="0.0.0.0", port=port)
