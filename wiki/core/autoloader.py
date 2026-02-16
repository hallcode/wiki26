import importlib
import os
import pkgutil
import wiki.modules
from flask.blueprints import Blueprint


class Autoloader:
    def __init__(self, app):
        self.app = app

    def boot(self):
        for module in self.scan():
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

    def find_extensions(self):
        pass
