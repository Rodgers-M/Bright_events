from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username

class Events(db.Model):
	"""This class represents the events table"""
	__tablename__ = 'events'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	created_by = db.Column(db.String(64))
	description = db.Column(db.Text)
	category = db.Column(db.String(64))
	location = db.Column(db.String(64))
	event_date = db.Column(db.DateTime)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	rsvps = db.relationship(User,
		secondary=rsvps,
		backref=db.backref('myrsvps', lazy='dynamic', cascade='all, delete-orphan'),
		lazy='dynamic')

	def add_rsvp(self, user):
		""" This method adds a user to the list of rsvps"""
		if not self.has_rsvp(user):
			self.rsvps.append(user)
			db.session.add(self)

	def has_rsvp(self, user):
		"""This method checks if a user is already registered for an event"""
		return self.rsvps.filter_by(
			id=user.id).first() is not None

	@staticmethod
	def get_all():
		"""a method to fetch all events"""
		return Events.query.all()

	@staticmethod
	def get_user_events(user):
		"""A method to return events belonging to a particular user"""
		all_events = Events.query.all()
		user_events = [event for event in all_events if event.created_by == user.username]
		return user_events

	def __repr__(self):
		return '<Events %r>' % self.name
