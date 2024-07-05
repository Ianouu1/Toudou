import os

from flask import Flask
import logging

from flask_httpauth import HTTPTokenAuth


def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui, api
    app.register_blueprint(web_ui)
    app.register_blueprint(api)

    app.config.from_prefixed_env(prefix="TOUDOU_FLASK")
    return app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("toudou.log"),
        logging.StreamHandler()
    ]
)

config = dict(
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True"
)