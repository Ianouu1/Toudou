from flask import Flask

def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui #add api later
    #app.register_blueprint(api)
    app.register_blueprint(web_ui)

    return app
    
config = dict(
    DATABASE_URL="sqlite:///data/mydata.db",
    DEBUG=True
)