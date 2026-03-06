import os

import tomllib
from flask import Flask

from wiki.core.assets import asset_manager
from wiki.core.authentication import login_manager
from wiki.core.autoloader import Autoloader
from wiki.core.cli import cli
from wiki.core.database import alembic, db
from wiki.core.views.login import auth_bp


def create_app():
    app = Flask(__name__)
    config_path = os.path.join(app.instance_path, "config.toml")
    app.config.from_file(config_path, load=tomllib.load, text=False)

    # Core
    app.register_blueprint(cli)
    app.register_blueprint(auth_bp)

    # Autoloader
    autoloader = Autoloader(app)
    autoloader.boot()
    autoloader.register_templates()

    # Database
    db.init_app(app)
    alembic.init_app(app)

    # For alembic mainly, but also to highlight errors early
    autoloader.load_models()

    # Authentication
    login_manager.init_app(app)

    # Resources
    asset_manager.init_app(app)

    return app
