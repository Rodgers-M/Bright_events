""" Import the create_app method, create the app and start the server"""
import os

from app import create_app

config_name = os.getenv('APP_SETTINGS') 
app = create_app(config_name)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run('', port=port) 
