from flask import Flask
from app import user, events, rsvp, middleware
from app.config import app_config

# Initialize flask app
app = Flask(__name__, instance_relative_config=True, template_folder='../designs/ui/templates', \
	static_folder='../designs/ui/static')
app.wsgi_app = middleware.PrefixMiddleware(app.wsgi_app, prefix='/api/v1')
#load from config.py in root folder
app.config.from_object(app_config['development'])
#load from config.py in instance folder
#app.config.from_pyfile('config.py')

#import the user, events and rsvp classes
user_object = user.User_details()
event_object = events.Events()
rsvp_object = rsvp.Rsvp()

#import the views
from app import views