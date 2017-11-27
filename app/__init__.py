from flask import Flask

# Initialize flask app
app = Flask(__name__, instance_relative_config=True)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'shhhssshhh'

from app import user, events

user_object = user.User_details()
event_object = events.Events()

from app import views