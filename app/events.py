#used to to validate event names
import re
from datetime import date
import uuid

class Events(object):
	""" A class to handle actions related to events"""

	def __init__(self):
		"""define an empty list to hold all the event objects"""
		self.event_list = []

	def existing_event(self, name, createdby, location):
		"""A method to check if a user already has that event in same location"""
		for event in self.event_list:
			#test to see if the user has the same event, in the same location in their list 
			if event['name'] == name and event['createdby'] == createdby:
				if event['location'] == location:
					return True
		else:
			return False

	def valid_name(self, name):
		"""check name length and special characters"""
		if len(name) < 3 or not re.match("^[a-zA-Z0-9_]*$", name):
			return False
		else:
			return True

	def create(self,name,description, category, location, event_date, createdby):
		"""A method for creating a new event"""

		self.event_details = {}
		if self.existing_event(name, createdby, location):
			return "event exists"	
		else:
			#validate event name
			if not self.valid_name(name):
				return "name too short or invalid"
			else:
				self.event_details['name'] = name
				self.event_details['description'] = description
				self.event_details['category'] = category
				self.event_details['location'] = location
				self.event_details['event_date'] = event_date
				self.event_details['date_created'] = date.today().isoformat()
				self.event_details['createdby'] = createdby
				self.event_details['id'] = uuid.uuid1()
				self.event_list.append(self.event_details)
				return "event created"

	def view_all(self):
		""" A method to return a list of all events"""
		return self.event_list
	
	def location_filter(self, location):
		"""A method to return a list of events in a certain location"""
		new_event_list = [event for event in self.event_list if event['location'] == location]
		return new_event_list

	def category_filter(self, category):
		"""A method to find events of a given category """
		new_event_list = [event for event in self.event_list if event['category'] == category]
		return new_event_list

	def update(self, eventid, name,description, category, location, event_date, createdby):
		""" Find an event with the given id and update its details"""
		for event in self. event_list:
			if event['id'] == eventid:
				if self.existing_event(name, createdby, location):
					return "Event cannot be updated, a similar event exists"
				else:
					if not self.valid_name(name):
						return "name too short or invalid"
					else:
						self.event_list.remove(event)
						event['name'] = name
						event['description'] = description
						event['category'] = category
						event['location'] = location
						event['event_date'] = event_date
						event['date_created'] = date.today().isoformat()
						event['createdby'] = createdby
						event['id'] = eventid
						self.event_list.append(self.event_details)
						return "update success"
			else:
				return "no event with given id"

	def delete(self, eventid):
		""" A method to delete an event from event list"""
		for event in self.event_list:
			if event['id'] == eventid:
				self.event_list.remove(event)
				return "deleted"
		else:
			return "error, event not found"





