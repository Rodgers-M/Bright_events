"""This module contains tests for the rsvp class"""
import unittest
from app.rsvp  import Rsvp
class TestRsvp(unittest.TestCase):
    """test class definitin and setup"""

    def setUp(self):
        """ Set up user object before each test"""
        self.rsvp = Rsvp()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.rsvp

    def test_create_success(self):
    	"""Test if the method works given a user id and event id"""
    	#use abitrary id's
    	res = self.rsvp.create(1234, 5678)
    	self.assertEqual(res, "rsvp success")

    def test_creating_same_rsvp_twice(self):
    	""" Test if a user can rsvp to the same event twice"""
    	self.rsvp.create(1234, 5678)
    	res = self.rsvp.create(1234, 5678)
    	self.assertEqual(res, "user already registered for event")

    def test_view_rsvp(self):
    	"""Test if the method returns a list with user id's"""
    	#Rsvp to the sane event with two different users
    	self.rsvp.create(1234, 5678)
    	self.rsvp.create(1234, 8765)
    	#call the view_rsvp method
    	id_list = self.rsvp.view_rsvp(1234)
    	self.assertEqual(id_list, [5678, 8765])
