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

	@staticmethod
	def get_all():
		"""a method to fetch all events"""
		return Events.query.all()

	def save(self):
		"""add the instance to session and save"""
		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return '<Events %r>' % self.name
