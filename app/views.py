import uuid
from app import app, user_object , event_object, rsvp_object
from flask import request, json , jsonify, url_for, session, render_template

#registration and login routes
@app.route('/auth/register', methods=['GET','POST'])
def register():
	"""A route to handle user"""
	if request.method == 'POST':
		user_details = request.get_json()
		username = user_details['username']
		email = user_details['email']
		password = user_details['password']
		cnfpassword = user_details['cnfpass']
		#pass the details to the register method
		res = user_object.register(username,email, password, cnfpassword)
		if res == "Registration successfull":
			return jsonify(response = res), 201
		else:
			return jsonify(response = res),409
	return jsonify(response="Get request currently not allowed"),405

@app.route('/auth/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		user_details = request.get_json()
		username = user_details['username']
		password = user_details['password']
		res = user_object.login(username, password)
		if res == "successful":
			for user in user_object.user_list:
				if user['username'] == username:
					session['userid'] = user['id']
					return jsonify(response ="login successful"), 200
		return res
	return jsonify(response="Get request currently not allowed"), 405

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
		if res == "event created":
			return jsonify(response=res), 201
		else:
			return jsonify(response = res), 409
	events = event_object.view_all()
	return jsonify(events), 200

@app.route('/events/<eventid>', methods = ['PUT'])
def update_event(eventid):
	"""A route to handle event updates"""
	eventid = uuid.UUID(eventid)
	event_details = request.get_json()
	name = event_details['name']
	description = event_details['description']
	category = event_details['category']
	location = event_details['location']
	event_date = event_details['event_date']
	createdby = event_details['createdby']
	res = event_object.update(eventid, name,description, category, location, event_date, createdby)
	if res == "update success":
		return jsonify(response = res), 200
	elif res == "no event with given id":
		return jsonify(response = res), 404
	else:
		return jsonify(response = res), 409

@app.route('/events/<eventid>', methods=['DELETE'])
def delete_event(eventid):
	"""A route to handle deletion of events"""
	eventid = uuid.UUID(eventid)
	res = event_object.delete(eventid)
	if res == "deleted":
		return jsonify(response="event deleted"), 204
	return jsonify(response = res), 404
	
@app.route('/event/<eventid>/rsvp', methods=['GET','POST'])
def rsvp(eventid):
	"""A route for registering a user to an event"""
	eventid = uuid.UUID(eventid)
	if request.method == 'POST':
		userid = session['userid']
		res = rsvp_object.create(eventid, userid)
		if res == "rsvp success":
			return jsonify(response=res), 200
		return jsonify(response =res), 304
	userids = rsvp_object.view_rsvp(eventid)
	users = [user for user in user_object.user_list if user['id'] in userids]
	return jsonify(users), 200
