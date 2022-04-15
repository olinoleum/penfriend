# Standard library imports

# Third Party imports
from flask import Flask

# Local application imports


def create_app():
    app = Flask(__name__)

    from penfriend.main.routes import main

    app.register_blueprint(main)

    return app
