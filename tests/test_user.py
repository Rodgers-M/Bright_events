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

    def test_existing_user(self):
        """TTest with an already existing user, try registering a user twice"""
        self.user.register("rodger", "654123", "654123")
        res = self.user.register("rodger", "654123", "654123")
        self.assertEqual(res, "Username already exists.")

    def test_password_length(self):
        res = self.user.register("random", "654", "654")
        self.assertEqual(res, "Password too short")

    def test_password_match(self):
        res = self.user.register("random", "654123", "1234654")
        self.assertEqual(res, "passwords do not match")

    def test_user_login(self):
        """Test if a user with valid details can login"""
        self.user.register("rodger", "654123", "654123")
        res = self.user.login("rodger", "654123")
        self.assertEqual(res, "successful")

    def test_wrong_password(self):
        """Test for a login attempt with a wrong password"""
        self.user.register("rodger", "654123", "654123")
        res = self.user.login("rodger", "65471234")
        self.assertEqual(res, "wrong password")

    def test_non_existing_user_login(self):
        """Test if a non-existing user can login"""
        self.user.register("rodger", "654123", "654123")
        res = self.user.login("mzungu", "654123")
        self.assertEqual(res, "user does not exist")

    
