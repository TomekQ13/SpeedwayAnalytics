from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from interface_api.config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from interface_api.routes import main
    app.register_blueprint(main)

    return app


