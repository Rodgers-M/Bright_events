from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
	# Initialize flask app
	app = Flask(__name__, instance_relative_config=True)

	#load from config.py in root folder
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	from .events import events as events_blueprint
	app.register_blueprint(events_blueprint, url_prefix='/events')
	return app
	