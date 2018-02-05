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
		res=self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		result = json.loads(res.data.decode())
		#assert that the request contains a success message and a 201 status code
		self.assertEqual(result['message'], "registration successful, now login")
		self.assertEqual(res.status_code, 201)

	def test_already_registered_user(self):
		"""Test app cannot registered same user twice."""
		res = self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		second_res = self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(second_res.status_code, 202)
		# get the results returned in json format
		result = json.loads(second_res.data.decode())
		self.assertEqual( result['message'], "email or username exists, please login or chose another username")

	def test_register_existing_email(self):
		"""try registering a user with existing email but unique username"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'different_username',
							'email' : 'test@example.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=another_user, content_type='application/json')
		self.assertIn('email or username exists', str(res.data))

	def test_register_existing_username(self):
		"""try registering a user with existing email but unique username"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'test_username',
							'email' : 'diff_test@example.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=another_user, content_type='application/json')
		self.assertIn('username exists', str(res.data))

	def test_register_invalid_email(self):
		"""try registering a user with invlid email"""
		invalid_user = json.dumps({
							'username' : 'test_username',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('please provide a valid email', str(res.data))

	def test_special_characters_in_email(self):
		"""try registering username with special characters"""
		invalid_user = json.dumps({
							'username' : 'username',
							'email' : 'test@example/.com',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('please provide a valid email', str(res.data))

	def test_missing_some_fields(self):
		"""test registering a user without a confirm password field"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		another_user = json.dumps({
							'username' : 'test_username',
							'email' : 'diff_test@example.com',
							'password' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=another_user, content_type='application/json')
		self.assertIn("please provide all the fields", str(res.data))

	def test_special_characters_in_username(self):
		"""try registering username with special characters"""
		invalid_user = json.dumps({
							'username' : '#username',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username  can only contain alphanumeric characters', str(res.data))

	def test_a_short_username(self):
		"""try registering a short username"""
		invalid_user = json.dumps({
							'username' : 'ab',
							'email' : 'test@example',
							'password' : 'test_password',
							'cnfpassword' : 'test_password'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('username must be more than 3 characters', str(res.data))

	def test_spaces_in_password(self):
		"""test registering a user with a password containing spaces"""
		invalid_user = json.dumps({
							'username' : 'username',
							'email' : 'test@example.com',
							'password' : 'test password',
							'cnfpassword' : 'test password'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('password should be one word, no spaces', str(res.data))

	def test_short_password(self):
		"""test registering a user with a short passsword"""
		invalid_user = json.dumps({
							'username' : 'username',
							'email' : 'test@example.com',
							'password' : 'test',
							'cnfpassword' : 'test'
						})
		res = self.client().post('/api/v2/auth/register', data=invalid_user, content_type='application/json')
		self.assertIn('Password should have atleast 6 characters', str(res.data))

	def test_existing_user_login(self):
		"""test an existing user can login"""
		res = self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		login_res = self.client().post('/api/v2/auth/login', data=self.user_data, content_type='application/json')
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
		res = self.client().post('/api/v2/auth/login', data=non_user,  content_type='application/json')
		result = json.loads(res.data.decode())
		#assert for the error message in response
		self.assertEqual(res.status_code, 401)
		self.assertEqual(result['message'], "invalid username or password, Please try again")

	def test_reset_password_works(self):
		"""test resetting a user password"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		res = self.client().post('/api/v2/auth/gettoken', data=self.user_data, content_type='application/json')
		token = json.loads(res.data.decode())['token']
		#send the new password along with the token
		data = json.dumps({
			"password" : "mynewpassword",
			"cnfpassword" : "mynewpassword",
			"token" : token
			})
		res = self.client().put('/api/v2/auth/resetpass', data=data, content_type='application/json' )
		self.assertIn("password reset successful", str(res.data))

	def test_user_can_login_using_new_password(self):
		"""test a user can login after resetting password"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		res = self.client().post('/api/v2/auth/gettoken', data=self.user_data, content_type='application/json')
		token = json.loads(res.data.decode())['token']
		#send the new password along with the token
		data = json.dumps({
			"password" : "mynewpassword",
			"cnfpassword" : "mynewpassword",
			"token" : token
			})
		self.client().put('/api/v2/auth/resetpass', data=data, content_type='application/json' )
		#re-assign  the password field to the new value
		new_user_data = json.dumps({
			'username' : 'test_username',
			'password' : 'mynewpassword'
			})
		res = self.client().post('/api/v2/auth/login', data=new_user_data, content_type='application/json')
		self.assertIn("login successful.", str(res.data))

	def test_user_can_not_login_using_old_password(self):
		"""test a user can not use old password after reset"""
		self.client().post('/api/v2/auth/register', data=self.user_data, content_type='application/json')
		res = self.client().post('/api/v2/auth/gettoken', data=self.user_data, content_type='application/json')
		token = json.loads(res.data.decode())['token']
		#send the new password along with the token
		data = json.dumps({
			"password" : "mynewpassword",
			"cnfpassword" : "mynewpassword",
			"token" : token
			})
		self.client().put('/api/v2/auth/resetpass', data=data, content_type='application/json' )
		#send request with data containing same old password 
		res = self.client().post('/api/v2/auth/login', data=self.user_data, content_type='application/json')
		self.assertIn("invalid username or password", str(res.data))