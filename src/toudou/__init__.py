import os

from flask import Flask, flash, redirect, url_for
import logging


def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui  #add api later
    #app.register_blueprint(api)
    app.register_blueprint(web_ui)
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