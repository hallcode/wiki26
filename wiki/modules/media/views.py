from flask import render_template

from . import media_bp


@media_bp.route("/")
def index():
    return render_template("media-index.html")
