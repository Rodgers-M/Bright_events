from app import app, user_object , event_object
from flask import request, json , jsonify, url_for, session
import uuid

@app.route('/')
def index():
	"""A route to render the home page"""
	return jsonify(message = "Hey, you are at index.")

#registration and login routes
@app.route('/auth/register', methods=['GET','POST'])
def register():
	"""A route to handle user"""
	if request.method == 'POST':
		user_details = request.get_json()
		username = user_details['username']
		password = user_details['password']
		cnfpass = user_details['cnfpass']
		#pass the details to the register method
		res = user_object.register(username, password, cnfpass)
		return res
	return jsonify(message = "Hmm, seems you want to register")

@app.route('/auth/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		user_details = request.get_json()
		username = user_details['username']
		password = user_details['password']
		res = user_object.login(username, password)
		return res
	return "The login page is coming soon"

#routes for events
@app.route('/events', methods = ['GET', 'POST'])
def events():
	if request.method == 'POST':
		event_details = request.get_json()
		name = event_details['name']
		description = event_details['description']
		category = event_details['category']
		location = event_details['location']
		event_date = event_details['event_date']
		createdby = event_details['createdby']
		res = event_object.create(name, description, category, location, event_date, createdby)
		print(event_object.event_list[0])
		return res
	events = event_object.view_all()
	return jsonify(events)

@app.route('/events/<eventid>', methods = ['PUT'])
def update_event(eventid):
	"""A route to handle event updates"""
	eventid = uuid.UUID(eventid)
	event_details = request.get_json()
	print(eventid)
	name = event_details['name']
	description = event_details['description']
	category = event_details['category']
	location = event_details['location']
	event_date = event_details['event_date']
	createdby = event_details['createdby']
	res = event_object.update(eventid, name,description, category, location, event_date, createdby)
	return res

@app.route('/events/<eventid>', methods=['DELETE'])
def delete_event(eventid):
	"""A route to handle deletion of events"""
	eventid = uuid.UUID(eventid)
	res = event_object.delete(eventid)
	return res

@app.route('/event/<eventid>/rsvp', methods=['POST'])
def rsvp(eventid):
	"""A route for registering a user to an event"""
	pass
