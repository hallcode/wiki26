from flask import Flask

from database import close_db
from wiki.core.autoloader import Autoloader

from wiki.core.views.login import auth_bp


def create_app():
    app = Flask(__name__)

    # Load core blueprints
    app.register_blueprint(auth_bp)

    # Load modules and extensions
    autoloader = Autoloader(app)
    autoloader.boot()
    autoloader.register_templates()

    # Close Database
    close_db(app)

    return app
