import os

from flask import Flask, flash, redirect, url_for


def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui  #add api later
    #app.register_blueprint(api)
    app.register_blueprint(web_ui)
    app.config.from_prefixed_env(prefix="TOUDOU_FLASK")
    @app.errorhandler(500)
    def handle_internal_error(error):
        flash("Erreur interne du serveur", "error")
        return redirect(url_for("web_ui.index"))

    return app


config = dict(
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True"
)