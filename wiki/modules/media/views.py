from . import media_bp


@media_bp.route("/")
def index():
    return "Hello (media) world"
