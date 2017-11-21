from flask import Flask

# Initialize flask app
app = Flask(__name__, instance_relative_config=True)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'shhhssshhh'