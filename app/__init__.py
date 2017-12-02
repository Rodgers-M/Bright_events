import os
from flask import Flask
from app import user, events, rsvp, middleware
from dotenv import load_dotenv, find_dotenv
from config import app_config


# Initialize flask app
app = Flask(__name__, instance_relative_config=True, template_folder='../designs/ui/templates', \
	static_folder='../designs/ui/static')
#load from config.py in root folder
app.config.from_object(app_config['production'])

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(find_dotenv())

#specify application route url
app.wsgi_app = middleware.PrefixMiddleware(app.wsgi_app, prefix='/api/v1')

#import the user, events and rsvp classes
user_object = user.User_details()
event_object = events.Events()
rsvp_object = rsvp.Rsvp()

#import the views
from app import views