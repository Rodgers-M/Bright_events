import unittest
import json
from datetime import date, timedelta
from app import create_app, db

class EventModelTest(unittest.TestCase):
	"""test the functionalities of the user model"""

	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client
		db.create_all()
		self.event_data = json.dumps({
				'name' : 'eventname',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'the space',
				'event_date' : str(date.today())
			})

		with self.app.app_context():
			db.session.close()
			db.drop_all()
			db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def  register_user(self, username='test_user', email='test@test.com',\
                passw='test_password', cnfpass='test_password'):
		"""helper function to register a user"""
		user_data = json.dumps({
				'username' : username,
				'email' : email,
				'password' : passw,
				'cnfpassword' : cnfpass
			})
		return self.client().post('/api/v2/auth/register', data=user_data,\
                        content_type='application/json')

	def  login_user(self, username='test_user', email='test@test.com',\
                passw='test_password', cnfpass='test_password'):
		"""helper function to login a user"""
		user_data = json.dumps({
				'username' : username,
				'email' : email,
				'password' : passw,
				'cnfpassword' : cnfpass
			})
		return self.client().post('/api/v2/auth/login', data=user_data, content_type='application/json')

	def get_access_token(self):
		"""register and login a user to get an access token"""
		self.register_user()
		result = self.login_user()
		access_token = json.loads(result.data.decode())['access_token']
		return access_token

	def test_create_event(self):
		"""test an event can be created successfully"""
		access_token = self.get_access_token()
		#create an event
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		self.assertIn('eventname', str(res.data))

	def test_creating_duplicate_events(self):
		"""assert if a user can create 2 events with same name and location"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		#try creating the same event again
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 302)

	def test_same_event_name_diff_location(self):
		"""test a user can create 2 events with same name but different location"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		result = json.loads(res.data.decode())
		self.assertEqual(result['location'], 'the space')
		#change the event location before sending another request
		self.event_data = json.dumps({
				'name' : 'eventname',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'another_location',
				'event_date' : str(date.today())
			})
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		result = json.loads(res.data.decode())
		self.assertEqual(result['location'], 'another_location')

	def test_short_event_name(self):
		"""test creating an event with a short event name"""
		access_token = self.get_access_token()
		event_data = json.dumps({
				'name' : 'nm',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'another_location',
				'event_date' : str(date.today())
			})
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=event_data, content_type='application/json')
		self.assertEqual(res.status_code, 400)
		self.assertIn("be at least 3 characters", str(res.data))

	def test_special_characters_in_data(self):
		"""test creating event with special characters in details"""
		access_token = self.get_access_token()
		event_data = json.dumps({
				'name' : 'eventname#',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'another_location',
				'event_date' : str(date.today())
			})
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=event_data, content_type='application/json')
		self.assertIn("should only contain alphanemeric characters", str(res.data))

	def test_past_date(self):
		"""test creating event with a past date"""
		access_token = self.get_access_token()
		event_data = json.dumps({
				'name' : 'eventname',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'another_location',
				'event_date' : str(date.today() - timedelta(days=1))
			})
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=event_data, content_type='application/json')
		self.assertIn("event cannot have a past date", str(res.data))

	def test_invalid_date(self):
		"""test creating event with invalid date format"""
		access_token = self.get_access_token()
		event_data = json.dumps({
				'name' : 'eventname',
				'description' : 'sample event description',
				'category' : 'event_testing',
				'location' : 'another_location',
				'event_date' : "2-12-2019"
			})
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=event_data, content_type='application/json')
		self.assertIn("incorrect date format", str(res.data))

	def test_user_with_invalid_token(self):
		"""assert if a user with invalid token can create an event"""
		access_token = self.get_access_token()
		#add a string to invalidate the token
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token + "spoil" ),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 401)
		self.assertIn('Please register or login', str(res.data))

	def test_user_without_a_token(self):
		"""test if a user without a token can create an event"""
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization=" "),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 401)
		self.assertIn('acess token is missing', str(res.data))

	def test_get_all_events(self):
		"""test if the api can fecth all events"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		res = self.client().get('/api/v2/events/all',
			headers=dict(Authorization="Bearer " + access_token), content_type='application/json')
		self.assertEqual(res.status_code, 200)
		result = json.loads(res.data.decode())
		self.assertEqual(result[0]['name'], 'eventname')

	def test_get_all_events_with_empty_db(self):
		"""fecth events when no events are created"""
		access_token = self.get_access_token()
		res = self.client().get('/api/v2/events/all',
			headers=dict(Authorization="Bearer " + access_token), content_type='application/json')
		self.assertIn('no events available', str(res.data))

	def test_get_user_events(self):
		"""test fecthing events belonging to a particular user"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		#register another user and create an event
		user2_data = json.dumps({
				'username' : 'test_user2',
				'email' :'	testemail2@testing.com',
				'password' : 'mypassword',
				'cnfpassword' : 'mypassword'
			})
		self.client().post('/api/v2/auth/register', data=user2_data, content_type='application/json')
		result = self.client().post('/api/v2/auth/login', data=user2_data, content_type='application/json')
		user2_access_token = json.loads(result.data.decode())['access_token']
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + user2_access_token),
			data=self.event_data, content_type='application/json')
		#fetch first user events
		res = self.client().get('/api/v2/events/myevents',
			headers=dict(Authorization="Bearer " + access_token), content_type='application/json')
		result = json.loads(res.data.decode())
		self.assertEqual(result[0]['orgarniser'], 'test_user')
		self.assertNotEqual(result[0]['orgarniser'], 'test_user2')
	def test_update_event(self):
		"""test if an event owner can update an event"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.assertEqual(res.status_code, 201)
		#update the event
		update_data =  json.dumps({
				'name' : 'new_event_name',
				'description' : 'real event description',
				'category' : 'event_update',
				'location' : 'another space',
				'event_date' : '2020-12-30'
			})
		#send update request
		res = self.client().put('/api/v2events/1',
			headers=dict(Authorization="Bearer " + access_token),
			data=update_data, content_type='application/json')
		self.assertEqual(res.status_code, 200)
		self.assertIn('event updated', str(res.data))

	def test_get_single_event(self):
		"""test user can get an event given its id"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		#fetch the event created
		res = self.client().get('/api/v2/events/1',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 200)

	def test_delete_event(self):
		"""test a user can delete an event"""
		access_token = self.get_access_token()
		res = self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		#delete the event
		res = self.client().delete('/api/v2/events/1',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 200)
		self.assertIn('event deleted', str(res.data))
		#try fetching the event after deletion
		res = self.client().get('/api/v2/events/1',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 404)

	def test_a_user_can_rsvp(self):
		"""test if a user can register to an event"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().post('/api/v2/events/1/rsvp',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 201)
		self.assertIn('rsvp success', str(res.data))

	def test_user_can_see_rsvp_list(self):
		"""test if a user can see rsvps to their events"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.client().post('/api/v2/events/1/rsvp',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		res = self.client().get('/api/v2/events/1/rsvp',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		result = json.loads(res.data.decode())
		self.assertEqual(result[0]['username'], 'test_user')

	def test_a_user_can_not_rsvp_twice(self):
		"""test if a user can register twice to one event"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		self.client().post('/api/v2/events/1/rsvp',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		res = self.client().post('/api/v2/events/1/rsvp',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 302)
		self.assertIn('already registered', str(res.data))

	def test_filter_by_location(self):
		"""test searching events by location works"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/filter?location=the space',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 200)
		self.assertIn('the space', str(res.data))

	def test_partial_location_filter(self):
		"""test searching by a partial location name"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/filter?location=space',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertIn('space', str(res.data))

	def test_filter_by_category(self):
		"""test searching events by category works"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/filter?category=event_testing',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 200)
		self.assertIn('event_testing', str(res.data))

	def test_invalid_filter(self):
		"""test filtering with invalid parameter"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/filter?description=event_testing',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 400)
		self.assertIn('can not search events with the given parameter', str(res.data))

	def test_search_by_full_name(self):
		"""test searching events by full name works"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/search?q=eventname',
			headers=dict(Authorization="Bearer " + access_token),
			content_type='application/json')
		self.assertEqual(res.status_code, 200)
		self.assertIn('eventname', str(res.data))

	def test_search_by_partial_name(self):
		"""test searching events by partial name works"""
		access_token = self.get_access_token()
		self.client().post('/api/v2/events/create',
			headers=dict(Authorization="Bearer " + access_token),
			data=self.event_data, content_type='application/json')
		res = self.client().get('/api/v2/events/search?q=event',
			headers=dict(Authorization="Bearer " + access_token))
		self.assertEqual(res.status_code, 200)
		self.assertIn('eventname', str(res.data))
