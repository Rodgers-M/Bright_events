#used to to validate event names
import re
from datetime import date

class Events(object):
	""" A class to handle actions related to events"""

	def __init__(self):
		"""define an empty list to hold all the event objects"""
		self.event_list = []

	def create(self,name,description, category, location, event_date, createdby):
		"""A method for creating a new event"""

		self.event_details = {}

		for event in self.event_list:
			#test to see if the user has the same event in their list 
			if event['createdby'] == createdby:
				#if event['createdby'] == createdby:
				return "event exists"
		else:
			#validate event name
			if len(name)< 3:
				return "name too short"
			elif not re.match("^[a-zA-Z0-9_]*$", name):
				return "event name can only be alphanumeric"
			else:
				self.event_details['name'] = name
				self.event_details['description'] = description
				self.event_details['category'] = category
				self.event_details['location'] = location
				self.event_details['event_date'] = event_date
				self.event_details['date_created'] = date.today().isoformat()
				self.event_details['createdby'] = createdby
				self.event_details['id'] = len(self.event_list) + 1
				self.event_list.append(self.event_details)
				return "event created"

	def delete(self, eventid):
		pass




