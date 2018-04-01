""" a module to handle all emailing in the app"""
from flask_mail import Message
from flask import current_app
from app import mail

def send_mail(receiver, subject, html):
    """a function to send emails from the app"""
    msg = Message(sender = current_app.config.get('MAIL_USERNAME'),recipient=[receiver])
    msg.subject = subject
    msg.html = html
    mail.send(msg)
    return "sent"
