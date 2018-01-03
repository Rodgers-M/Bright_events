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
		event = Events(name=name, description=description, category=category, \
			location=location, event_date=event_date, created_by=created_by)
		event.save()
		res = {
			"id" : event.id,
			"name" : event.name,
			"date_created" : event.date_created,
			"created_by" : event.created_by.username
			}
		return jsonify(res), 201
	return jsonify({"message" : "please login or register to create an event"})
	