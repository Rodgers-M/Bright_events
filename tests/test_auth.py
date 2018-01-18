import unittest
from flask import json
from app import create_app, db

class AuthTest(unittest.TestCase):
	"""Tests for the authentication blueprint."""
	def setUp(self):
		"""setup test variables"""
		self.app = create_app(config_name='testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client
		self.user_data = json.dumps({
							'username' : 'test_username',
							'email' : 'test@example.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})

		with self.app.app_context():
			db.session.close()
			db.drop_all()
			db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
		del self.client

	def test_registration(self):
		"""Test user registration works correcty."""
		res=self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		result = json.loads(res.data.decode())
		#assert that the request contains a success message and a 201 status code
		self.assertEqual(result['message'], "registration successful, now login")
		self.assertEqual(res.status_code, 201)

	def test_already_registered_user(self):
		"""Test app cannot registered same user twice."""
		res = self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		second_res = self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(second_res.status_code, 202)
		# get the results returned in json format
		result = json.loads(second_res.data.decode())
		self.assertEqual( result['message'], "email or username exists, please login or chose another username")

	def test_register_existing_email(self):
		"""try registering a user with existing email but unique username"""
		self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'different_username',
							'email' : 'test@example.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=another_user, content_type='application/json')
		self.assertIn('email or username exists', str(res.data))

	def test_register_existing_username(self):
		"""try registering a user with existing email but unique username"""
		self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'test_username',
							'email' : 'diff_test@example.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=another_user, content_type='application/json')
		self.assertIn('username exists', str(res.data))

	def test_register_invalid_email(self):
		"""try registering a user with invlid email"""
		invalid_user = json.dumps({
							'username' : 'test_username',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username or email must be valid', str(res.data))

	def test_special_characters_in_email(self):
		"""try registering username with special characters"""
		invalid_user = json.dumps({
							'username' : 'username',
							'email' : 'test@example/.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username or email must be valid', str(res.data))

	def test_missing_some_fields(self):
		"""test registering a user without a confirm password field"""
		self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'test_username',
							'email' : 'diff_test@example.com',
							'password' : 'test_password'
						})
		res = self.client().post('/auth/register', data=another_user, content_type='application/json')
		self.assertIn("please provide all the fields", str(res.data))

	def test_special_characters_in_username(self):
		"""try registering username with special characters"""
		invalid_user = json.dumps({
							'username' : '#username',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username or email must be valid', str(res.data))

	def test_a_short_username(self):
		"""try registering a short username"""
		invalid_user = json.dumps({
							'username' : 'ab',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username or email must be valid', str(res.data))

	def test_short_password(self):
		"""test registering a user with a short passsword"""
		invalid_user = json.dumps({
							'username' : 'username',
							'email' : 'test@example.com',
							'password' : 'test',
							'cnfpassword' : 'test'
						})
		res = self.client().post('/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('Password too short', str(res.data))
	def test_existing_user_login(self):
		"""test an existing user can login"""
		res = self.client().post('/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		login_res = self.client().post('/auth/login', data=self.user_data, content_type='application/json')
		result = json.loads(login_res.data.decode())
		self.assertEqual(result['message'], "login successful.")
		#assert the status code is 200
		self.assertEqual(login_res.status_code, 200)
		self.assertTrue(result['access_token'])

	def test_non_existing_user_login(self):
		"""test that a non-existing user cannot login"""
		#a non-existing user details
		non_user = json.dumps({
			'username' : 'unknown',
			'password' : 'password'
			})
		res = self.client().post('/auth/login', data=non_user,  content_type='application/json')
		result = json.loads(res.data.decode())
		#assert for the error message in response
		self.assertEqual(res.status_code, 401)
		self.assertEqual(result['message'], "invalid username or password, Please try again")