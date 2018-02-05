from flask_mail import Message
from flask import current_app
from app import mail

def send_mail(to):
	"""a function to send emails from the app"""
	msg = Message("Bright Events", 
		sender = current_app.config.get('MAIL_USERNAME'),
		recipients=[to] )
	msg.body = "registration successful"
	mail.send(msg)
	return "sent"