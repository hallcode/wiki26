import importlib
import os
import pkgutil
from tempfile import template

from jinja2 import ChoiceLoader, FileSystemLoader

import wiki.modules
from flask.blueprints import Blueprint


class Autoloader:
    def __init__(self, app):
        self.app = app
        self.modules = self.scan()

    def boot(self):
        for module in self.modules:
            modules = dir(module)
            modules = list(filter(lambda x: not x.startswith("__"), modules))
            for attr in modules:
                bp = getattr(module, attr)
                if not isinstance(bp, Blueprint):
                    continue

                try:
                    importlib.import_module(module.__name__ + ".views")

                except ModuleNotFoundError as e:
                    if e.name != module.__name__ + ".views":
                        raise

                self.app.register_blueprint(bp)

    def scan(self):
        modules = []

        for _, module_name, _ in pkgutil.iter_modules(wiki.modules.__path__):
            full_name = f"wiki.modules.{module_name}"
            module = importlib.import_module(full_name)
            modules.append(module)

        return modules

    def register_templates(self):
        loader = ChoiceLoader([self.app.jinja_loader])

        # Load the core module templates folder
        core_module = importlib.import_module("wiki.core")
        core_template_dir = os.path.join(
            os.path.dirname(core_module.__file__), "templates"
        )
        if os.path.isdir(core_template_dir):
            loader.loaders.append(FileSystemLoader(core_template_dir))

        # Search for and load module template folders
        for module in self.modules:
            module_template_dir = os.path.join(
                os.path.dirname(module.__file__), "templates"
            )
            if os.path.isdir(module_template_dir):
                loader.loaders.append(FileSystemLoader(module_template_dir))

        # Register on the app
        self.app.jinja_loader = loader

    def find_extensions(self):
        pass
