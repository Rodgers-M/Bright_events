import unittest
import json
from datetime import datetime
from app import create_app, db
from app.models import User

class UserModelTest(unittest.TestCase):
	"""test the functionalities of the user model"""

	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client
		db.create_all()
		self.user_data = json.dumps({
				'username' : 'test_user',
				'email' : 'test@test.com',
				'password' : 'test_password'
			})
		self.event_data = json.dumps({
				'name' : 'eventname',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'the space',
				'event_date' : '2019-12-30'
			})

		with self.app.app_context():
			db.session.close()
			db.drop_all()
			db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def  register_user(self, username='test_user', email='test@test.com', password='test_password'):
		"""helper function to register a user"""
		user_data = json.dumps({
				'username' : username,
				'email' : email,
				'password' : password
			})
		return self.client().post('/auth/register', data=user_data, content_type='application/json')

	def  login_user(self, username='test_user', email='test@test.com', password='test_password'):
		"""helper function to login a user"""
		user_data = json.dumps({
				'username' : username,
				'email' : email,
				'password' : password
			})
		return self.client().post('/auth/login', data=user_data, content_type='application/json')

	def test_create_event(self):
		"""test an event can be created successfully"""
		self.register_user()
		result = self.login_user()
		#get the access_token to be sent with the request
		access_token = json.loads(result.data.decode())['access_token']
		#create an event
		res = self.client().post('/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		self.assertIn('eventname', str(res.data))

