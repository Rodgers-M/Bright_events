""" Import the app and start the server"""
import os
from app import app

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run('', port=port) 