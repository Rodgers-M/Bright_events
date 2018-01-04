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