from flask import Blueprint

cli = Blueprint("cli", __name__, cli_group="wiki")

from . import user
