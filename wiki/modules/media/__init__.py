from flask import Blueprint
import os

media_bp = Blueprint(
    "media",
    __name__,
    url_prefix="/media",
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)
