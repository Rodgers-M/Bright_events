import unittest
from app.user import User_details


class UserTests(unittest.TestCase):

    def setUp(self):
        """ Set up user object before each test"""
        self.user = User_details()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    def test_isuccessful_registration(self):
        """Test is a user with correct credentials can register sucessfully"""
        res = self.user.register("rodger", "654123", "654123")
        self.assertEqual(res, "Registration successfull")