from flask import request, jsonify,g
from app.models import Events
from . import events
@events.route('/create', methods=['POST'])
def create():
	"""a route to handle creating an event"""
	if g.user:
		event_details = request.get_json()
		name = event_details['name']
		description = event_details['description']
		category = event_details['category']
		location = event_details['location']
		event_date = event_details['event_date']
		created_by = g.user
		#check if the user has an event with a similar name and location
		existing_event = [event for event in g.user.events if event.name == name \
			and event.location == location]
		if not existing_event:
			#create the event if does not exist
			event = Events(name=name, description=description, category=category, \
				location=location, event_date=event_date, created_by=created_by)
			event.save()
			res = {
				"id" : event.id,
				"name" : event.name,
				"category" : event.category,
				"created_by" : event.created_by.username,
				"location" : event.location,
				"date_created" : event.date_created
				}
			return jsonify(res), 201
		return jsonify({"message" : "you have a similar event in the same location"}), 302
	return jsonify({"message" : "please login or register  to create an event"}), 401

@events.route('/all')
def get_all():
	"""fetch all events available"""
	if g.user:
		events = Events.get_all()
		if events:
			event_list = []
			for event in events:
				evnt = {
					"id" : event.id,
					"name" : event.name,
					"description" : event.description,
					"category" : event.category,
					"location" : event.location,
					"created_by" : event.created_by.username,
					"event_date" : event.event_date,
					"date_created" : event.date_created
				}
				event_list.append(evnt)
			return jsonify(event_list), 200
		return jsonify({"message" : "no events created yet"}), 200
	return jsonify({"message" : "please login or register view events"}), 401

@events.route('/myevents')
def my_events():
	"""fetch all events belonging to a particular user"""
	if g.user:
		events = g.user.events
		if events:
			event_list = []
			for event in events:
				evnt ={
					"id" : event.id,
					"name" : event.name,
					"description" : event.description,
					"category" : event.category,
					"location" : event.location,
					"created_by" : event.created_by.username,
					"event_date" : event.event_date,
					"date_created" : event.date_created
				}
				event_list.append(evnt)
			return jsonify(event_list), 200
		return jsonify({"message" : "you have not created any events yet"}), 200
	return jsonify({"message" : "please login to access your events"}), 401

@events.route('/<int:event_id>', methods=['PUT', 'DELETE' , 'GET' ])
def manipulate_event(event_id):
	"""update or delete an event"""
	if g.user:
		event = Events.get_event_by_id(event_id)
		if event:
			#maeke sure the events is modified by the right person
			if event.created_by.username == g.user.username:
				if request.method == 'PUT':
				#get the incoming details 
					event_details = request.get_json()
					#update the details accordingly
					event.name = event_details['name']
					event.description = event_details['description']
					event.category = event_details['category']
					event.location = event_details['location']
					event.event_date = event_details['event_date']
					#save the event back to the database
					event.save()
					return jsonify({"message" : "event updated successfully"}), 200
				elif request.method == 'GET':
					#return the event with the given id
					found_event = {
						'id' : event.id,
						'description' : event.description,
						'category' : event.category,
						'location' : event.location,
						'created_by' : event.created_by.username,
						'event date' : event.event_date,
						'date created' : event.date_created
					}
					return jsonify(found_event), 200
				else:
				#if the request method is delete
					event.delete()
					return jsonify({"message" : "event deleted successfully"}), 200
			return jsonify({"message" : "you can not modify the event"})
		return jsonify({"message" : "no event with given id found"}), 404
	return jsonify({"message" : "please login or register  to create an event"}), 401

@events.route('/<int:event_id>/rsvp', methods=['POST', 'GET'])
def rsvp(event_id):
	"""register a user to an event"""
	if g.user:
		event = Events.get_event_by_id(event_id)
		if event:
			if request.method == 'POST':
				res = event.add_rsvp(g.user)
				if res == "rsvp success":
					return jsonify({"message" : "rsvp success, see you then"}), 201
				return jsonify({"message" : "already registered for this event"}), 302
			rsvps = event.rsvps.all()
			if rsvps:
				rsvp_list = []
				for user in rsvps:
					rsvp= {
						"username" : user.username,
						"email" : user.email
					}
					rsvp_list.append(rsvp)
				return jsonify(rsvp_list), 200
			return jsonify({"message" : "no users have responded to this event yet"}),200
		return jsonify({"message" : "event does not exist"}), 404
	return jsonify({"message" : "please login or signup to rsvp"}), 401

@events.route('/myrsvps')
def my_rsvps():
	"""return the list of events that user has responded to"""
	if g.user:
		rsvps = g.user.myrsvps.all()
		if rsvps:
			rsvp_list = []
			for event in rsvps:
				rsvp = {
					"event name" : event.name,
					"location" : event.location,
					"orgarniser" : event.created_by.username,
					"event date" : event.event_date
				}
				rsvp_list.append(rsvp)
			return jsonify(rsvp_list), 200
		return jsonify({"message" : "you have not responded to any events yet"}), 200
	return jsonify({"message" : "please login or signup to see your rsvps"}), 401





