# Standard library imports
import logging
import os

# Third Party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from dotenv import load_dotenv

# Local application imports


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True


load_dotenv('penfriend/.env')

uri = os.environ.get("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap4')


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    logging.basicConfig(level=logging.DEBUG)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    admin.init_app(app)

    @app.before_first_request
    def create_tables():
        from penfriend.models import User, Message
        with app.app_context():
            db.create_all()

    from penfriend.main.routes import main
    from penfriend.adminbp.routes import adminblueprint
    from .commands import create_tables

    app.register_blueprint(main)
    app.register_blueprint(adminblueprint)
    app.cli.add_command(create_tables)

    return app
