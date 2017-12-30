import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
	# Initialize flask app
	app = Flask(__name__, instance_relative_config=True, template_folder='../designs/ui/templates', \
		static_folder='../designs/ui/static')

	#load from config.py in root folder
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	return app
	