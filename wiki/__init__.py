from flask import Flask
from wiki.core.autoloader import Autoloader

from wiki.core.views.authentication import auth_bp


def create_app():
    app = Flask(__name__)

    # Load core blueprints
    app.register_blueprint(auth_bp)

    # Load modules and extensions
    autoloader = Autoloader(app)
    autoloader.boot()
    autoloader.register_templates()

    return app
