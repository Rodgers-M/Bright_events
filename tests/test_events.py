import unittest
from app.events import Events


class Event_tests(unittest.TestCase):

    def setUp(self):
        """ Set up user object before each test"""
        self.event = Events()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.event

    def test_create_event_works(self):
    	"""Test that with correct event details the method works"""

    	res = self.event.create("hackathon", "get experience", "technology", "the space", 26/11/2017, "rodger")
    	self.assertEqual(res, "event created")

    def test_crete_existing_event(self):
    	""" Test if an evnt can be cr"eated twice"""
    	
    	self.event.event_list =[{"name" :'hackathon', "description" :'get experience', "category":'technology', \
    		 "location":'the space', "date" : 26/11/2017, "createdby":'rodger'}]
    	res = self.event.create("hackathon", "get experience", "technology", "the space", 26/11/2017, "rodger")
    	self.assertEqual(res, "event exists")

    def test_event_name_length(self):
    	""" Test if one can create an event with less than 3 characters"""
    	res = self.event.create('ab', 'get experience', 'technology', 'the space', 26/11/2017, 'rodger')
    	self.assertEqual(res, "name too short")

    def test_first_event_id(self):
    	""" Test if id's are generated correctly"""
    	self.event.create("hackathon", "get experience", "technology", "the space", 26/11/2017, "rodger")
    	id = self.event.event_list[0]['id']
    	self.assertEqual(id, 1)



