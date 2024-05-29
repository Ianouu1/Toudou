from flask import Flask

def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui #add api later
    #app.register_blueprint(api)
    app.register_blueprint(web_ui)

    return app
    
config = dict(
    DATABASE_URL="sqlite:///mydata.db",
    DEBUG=True
    # DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    # DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True"
)