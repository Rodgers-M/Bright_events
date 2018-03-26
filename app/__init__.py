from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import app_config
from app.errorhandler import not_found, bad_request, internal_server_error

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    # Initialize flask app
    app = Flask(__name__, instance_relative_config=True)

    #load from config.py in root folder
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    mail.init_app(app)
    from .api_v2 import api as api_v2_blueprint
    app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, internal_server_error)
    return app
	
