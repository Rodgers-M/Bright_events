from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from datetime import datetime, timedelta
from app import db

rsvps = db.Table('rsvps',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
	)

class User(db.Model):
	"""this class to defines the user data model"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(128))
	events = db.relationship('Events', backref='created_by', cascade="all, delete-orphan")
	myrsvps = db.relationship('Events',
		secondary=rsvps,
		backref=db.backref('rsvps', lazy='dynamic'),
		lazy='dynamic')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def save(self):
		"""add user instance to session and save to databas"""
		db.session.add(self)
		db.session.commit()

	def generate_token(self, user_id):
		"""a method to generate the access token"""
		try:
			# set up a payload
			payload={
				'exp': datetime.utcnow() + timedelta(minutes=10),
				'iat': datetime.utcnow(),
				'sub': user_id
			}
			# create the byte string token using the payload and the SECRET key
			jwt_string = jwt.encode(
				payload,
				current_app.config.get('SECRET_KEY'),
				algorithm='HS256'
			)
			return jwt_string

		except Exception as e:
			# return an error in string format if an exception occurs
			return str(e)

	@staticmethod
	def decode_token(token):
		"""Decodes the access token from the Authorization header."""
		try:
			# try to decode the token using our SECRET variable
			payload = jwt.decode(token, current_app.config.get('SECRET'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			# the token is expired, return an error string
			return "Expired token. Please login to get a new token"
		except jwt.InvalidTokenError:
			# the token is invalid, return an error string
			return "Invalid token. Please register or login"

	def __repr__(self):
		return '<User %r>' % self.username

class Events(db.Model):
	"""This class represents the events table"""
	__tablename__ = 'events'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	name = db.Column(db.String(64))
	description = db.Column(db.Text)
	category = db.Column(db.String(64))
	location = db.Column(db.String(64))
	event_date = db.Column(db.DateTime)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	

	def add_rsvp(self, user):
		""" This method adds a user to the list of rsvps"""
		if not self.has_rsvp(user):
			self.rsvps.append(user)
			db.session.add(self)

	def has_rsvp(self, user):
		"""This method checks if a user is already registered for an event"""
		return self.rsvps.filter_by(
			id=user.id).first() is not None

	def save(self):
		"""add the instance to session and save"""
		db.session.add(self)
		db.session.commit()

	def delete(self):
		"""delete a particular event"""
		db.session.delete(self)
		db.session.commit()

	@staticmethod
	def get_all():
		"""a method to fetch all events"""
		return Events.query.all()

	def __repr__(self):
		return '<Events %r>' % self.name
