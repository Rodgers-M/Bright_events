import os
from flask import Flask
from app import user, events, rsvp, middleware
from config import app_config

#import the user, events and rsvp classes
user_object = user.User_details()
event_object = events.Events()
rsvp_object = rsvp.Rsvp()

def create_app(config_name):
	# Initialize flask app
	app = Flask(__name__, instance_relative_config=True, template_folder='../designs/ui/templates', \
		static_folder='../designs/ui/static')
	#load from config.py in root folder
	app.config.from_object(app_config[config_name])

	#specify application route url
	app.wsgi_app = middleware.PrefixMiddleware(app.wsgi_app, prefix='/api/v1')

	from app.main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app
	