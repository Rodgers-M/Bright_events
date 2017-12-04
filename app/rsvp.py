class Rsvp(object):
	"""a class to handle RSVPs"""

	def __init__(self):
		self.rsvp_list = []

	def create(self, event_id, user_id):
		""" register a user to an event"""
		self.rsvp_details = {}
		for rsvp in self.rsvp_list:
			if rsvp['event_id'] == event_id and rsvp['user_id'] == user_id:
				return "user already registered for event"
		else:
			self.rsvp_details['event_id'] = event_id
			self.rsvp_details['user_id'] = user_id
			self.rsvp_list.append(self.rsvp_details)
			return "rsvp success"

	def view_rsvp(self, event_id):
		""" 
		Get the user id's of users who have responded to an event
		These will be passed to the user object to retrieve the user details
		"""
		user_ids = [rsvp['user_id'] for rsvp in self.rsvp_list if rsvp['event_id'] == event_id]
		return user_ids


		