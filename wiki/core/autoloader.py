import importlib
import os
from flask.blueprints import Blueprint


class Autoloader:
    def __init__(self, app):
        self.app = app

    def boot(self):
        modules = self.scan()

        # Scan modules and register any blueprints.
        for module in modules:
            sub_modules = dir(module)
            sub_modules = filter(lambda x: not x.startswith("__"), sub_modules)
            for name in sub_modules:
                bp = getattr(module, name)
                if not isinstance(bp, Blueprint):
                    continue

                try:
                    importlib.import_module(module.__name__ + ".views")
                except ImportError:
                    continue
                self.app.register_blueprint(bp)


    def scan(self):
        """
        Find all the python packages in the modules package
        i.e. scan and find the feature modules
        :return:
        """
        modules = []

        basepath = os.path.join(os.getcwd(), "wiki", "modules")
        for file in os.scandir(basepath):
            if file.is_file():
                continue

            if file.name.startswith("__"):
                continue

            try:
                module_name = "wiki.modules." + file.name
                m = importlib.import_module(module_name)
                modules.append(m)

            except ImportError:
                print("Unable to import module: " + module_name)

        return modules

    def find_extensions(self):
        """
        Find all the app extensions in each module
        :return: { name: str, type: str, ext: Any }
        """
        pass
