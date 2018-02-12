from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import date
from sqlalchemy import cast , Date
from flask import current_app
from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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

	def generate_auth_token(self):
		"""a method to generate the access token"""
		try:
			# set up a payload
			payload={
				'exp': datetime.utcnow() + timedelta(minutes=60),
				'iat': datetime.utcnow(),
				'sub': self.id
			}
			# create the byte string token using the payload and the SECRET key
			jwt_string = jwt.encode(
				payload,
				current_app.config.get('SECRET_KEY'),
				algorithm='HS256'
			)
			return jwt_string

		except Exception as error:
			# return an error in string format if an exception occurs
			return str(error)

	@staticmethod
	def decode_auth_token(token):
		"""Decodes the access token from the Authorization header."""
		try:
			# try to decode the token using our SECRET variable
			payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			# the token is expired, return an error message
			return "you were logged out. Please login"
		except jwt.InvalidTokenError:
			# the token is invalid, return an error message
			return "Please register or login"

	def generate_confirmation_token(self, expiration=1800):
		"""generate a token for confiming user emails, valid for 30 min by default"""
		serializer = Serializer(current_app.config.get('SECRET_KEY'), expires_in=expiration)
		return serializer.dumps({'conf_email': self.email})

	@staticmethod
	def decode_confirmation_token(token):
		"""trydecoding the token and fetch the user"""
		serializer = Serializer(current_app.config.get('SECRET_KEY'))
		try:
			data = serializer.loads(token)
		except Exception:
			#the token is either invalid or expired
			return "invalid or expired token"
		user = User.query.filter_by(email=data.get('conf_email')).first()
		return user

	#this will be used to test pagination
	@staticmethod
	def generate_fake_users(count=20):
		"""try genarating 20 fake users"""
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			user  = User(username=forgery_py.internet.user_name(True),
					email=forgery_py.internet.email_address(),
					password=forgery_py.lorem_ipsum.word())
			db.session.add(user)
			try:
				#try saving the user to db
				db.session.commit()
			except IntegrityError:
				#if generated email or username already exists
				db.session.rollback()

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
			self.save()
			return "rsvp success"
		return "already registered"

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

	def to_json(self):
		"""convert a given event to json"""
		json_event ={
					"id" : self.id,
					"name" : self.name,
					"description" : self.description,
					"category" : self.category,
					"location" : self.location,
					"orgarniser" : self.created_by.username,
					"event date" : self.event_date,
					"date created" : self.date_created
				}
		return json_event

	@staticmethod
	def get_event_by_id(event_id):
		"""get an event with the given id"""
		return Events.query.filter_by(id=event_id).first()

	@staticmethod
	def get_events_by_category(category, page, per_page):
		"""filter events by category"""
		return Events.query.filter(Events.category.ilike("%" + category + "%"))\
		.filter(cast(Events.event_date, Date) >=  date.today())\
		.order_by(Events.event_date.desc()).paginate(page, per_page, error_out=False)

	@staticmethod
	def get_events_by_location(location, page, per_page):
		"""filter events by location"""
		return Events.query.filter(Events.location.ilike("%" + location + "%"))\
		.filter(cast(Events.event_date, Date) >=  date.today())\
		.order_by(Events.event_date.desc())\
                .paginate(page, per_page, error_out=False)

	@staticmethod
	def filter_events(location, category, page, per_page):
		"""filter events by both category and location"""
		return Events.query.filter(Events.location.ilike("%" + location + "%"))\
            .filter(Events.category.ilike("%" + category + "%"))\
			.filter(cast(Events.event_date, Date) >=  date.today())\
			.order_by(Events.event_date.desc())\
                        .paginate(page, per_page, error_out=False)

	@staticmethod
	def get_events_by_name(name, page, per_page):
		"""filter events by name"""
		return Events.query.filter(Events.name.ilike("%" + name + "%"))\
		.order_by(Events.event_date.desc()).paginate(page, per_page, error_out=False)

	#this will be used to test pagination
	@staticmethod
	def generate_fake_events(count=100):
		"""generate 100 fake events"""
		import random
		import forgery_py

		random.seed()
		categories = ["technology", "social", "education", "family"]
		user_count = User.query.count()
		for i in range(count):
			#pick a random user to be the event creator
			user = User.query.offset(random.randint(0, user_count - 1)).first()
			event = Events(name=forgery_py.lorem_ipsum.word(),
					description=forgery_py.lorem_ipsum.sentences(),
					category=random.choice(categories),
					location=forgery_py.address.city(),
					event_date = forgery_py.date.date(True),
					created_by = user
					)
			db.session.add(event)
			db.session.commit()

	def __repr__(self):
		return '<Events %r>' % self.name

class BlacklistToken(db.Model):
    """class to handle token blacklisting"""
    __tablename__ = "blacklist_tokens"
    id =  db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True)
    blacklisted_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, token):
        """initialize the class with a token"""
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        res = BlacklistToken.query.filter_by(token=token).first()
        if res:
        	return True
        return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
