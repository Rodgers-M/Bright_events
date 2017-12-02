"""Module contains tests for the events class"""
import unittest
from app.events import Events


class Event_tests(unittest.TestCase):
    """Class definitin and setup"""

    def setUp(self):
        """ Set up user object before each test"""
        self.event = Events()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.event

    def test_create_event_works(self):
    	"""Test that with correct event details the method works"""

    	res = self.event.create("hackathon", "get experience", \
            "technology", "the space", 26/11/2017, "rodger")
    	self.assertEqual(res, "event created")

    def test_crete_existing_event(self):
    	""" Test if an event can be created twice"""
    	
    	self.event.event_list = [{"name" :'hackathon', "description" :'get experience',\
         "category":'technology',  "location":'the space', \
         "date" : 26/11/2017, "createdby":'rodger'}]
    	res = self.event.create("hackathon", "get experience", \
            "technology", "the space", 26/11/2017, "rodger")
    	self.assertEqual(res, "event exists")

    def test_same_event_diff_location(self):
    	""" Test if a user can create the same event but in different locations"""
    	self.event.event_list = [{"name" :'hackathon', \
            "description" :'get experience', "category":'technology', \
    		 "location":'the space', "date" : 26/11/2017, "createdby":'rodger'}]
    	res = self.event.create("hackathon", "get experience", "technology", \
            "the office", 26/11/2017, "rodger")
    	self.assertEqual(res, "event created")

    def test_event_name_length(self):
    	""" Test if one can create an event with less than 3 characters"""
    	res = self.event.create('ab', 'get experience', 'technology', \
            'the space', 26/11/2017, 'rodger')
    	self.assertEqual(res, "name too short or invalid")

    def test_category_filter(self):
    	"""Test if filter lcategory works"""
    	self.event.create("hackathon", "get experience", "technology", \
            "the office", 26/11/2017, "rodger")
    	self.event.create("marathon", "run", "sports", "ndakaini", 26/11/2017, "rodger")
    	res = self.event.category_filter("sports")
    	event_name = res[0]['name']
    	self.assertIs(event_name, "marathon")
    	self.assertIsNot(event_name, "hackathon")
    	self.assertEqual(len(res), 1)
    	self.assertIsInstance(res, list)

    def test_location_filter(self):
    	"""Test if filter location works"""
    	self.event.create("hackathon", "get experience", "technology", \
            "the office", 26/11/2017, "rodger")
    	self.event.create("marathon", "run", "sports", "ndakaini", 26/11/2017, "rodger")
    	res = self.event.location_filter("ndakaini")
    	event_name = res[0]['name']
    	self.assertIs(event_name, "marathon")
    def test_delete(self):
    	"""Test if given an id the method will delete an event"""
    	self.event.create("marathon", "run", "sports", "ndakaini", 26/11/2017, "rodger")
    	event_id = self.event.event_list[0]['id']
    	res = self.event.delete(event_id)
    	self.assertIs(res, "deleted")
    	self.assertEqual(len(self.event.event_list), 0)

    def test_update(self):
    	"""Test if method can update an event successfully"""
    	self.event.create("marathon", "run", "sports", "ndakaini", 26/11/2017, "rodger")
    	event_id = self.event.event_list[0]['id']
    	#update the location
    	res = self.event.update(event_id, "marathon", "run", "sports",\
            "mombasa", 26/11/2017, "rodger")
    	self.assertEqual(res, "update success")
    	#check if the location has been updated
    	new_location = self.event.event_list[0]['location']
    	self.assertIs(new_location, "mombasa")
    	#check if the id is still the same after update
    	new_id = self.event.event_list[0]['id']
    	self.assertEqual(event_id, new_id)

    def test_find_by_id_works(self):
        """Test if the method finds the exactly specified id"""
        self.event.create("marathon", "run", "sports", "ndakaini", 26/11/2017, "rodger")
        event_id = self.event.event_list[0]['id']
        eventname = self.event.event_list[0]['name']
        foundevent = self.event.find_by_id(event_id)
        self.assertEqual(foundevent['name'], eventname)








   
