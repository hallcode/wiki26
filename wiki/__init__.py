from flask import Flask
from wiki.core.autoloader import Autoloader


def create_app():
    app = Flask(__name__)

    autoloader = Autoloader(app)
    autoloader.boot()

    return app
