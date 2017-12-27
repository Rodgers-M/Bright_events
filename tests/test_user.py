"""This module defines tests for the user class and its methods"""
import unittest
from app.user import UserDetails

class UserTests(unittest.TestCase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up user object before each test"""
        self.user = UserDetails()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    def test_successful_registration(self):
        """Test is a user with correct credentials can register sucessfully"""
        res = self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        self.assertEqual(res, "Registration successfull")

    def test_special_characters_in_username(self):
        """Test registering a username with special characters"""
        res = self.user.register("rodger*#", "rodger@mail.com", "654123", "654123")
        self.assertEqual(res, "Username or email can only contain alphanumeric characters")

    def test_special_characters_in_email(self):
        """Test registering an email with special characters"""
        res = self.user.register("rodger", "rodge#r@mail.com", "654123", "654123")
        self.assertEqual(res, "Username or email can only contain alphanumeric characters")

    def test_register_invalid_email(self):
        """Test registering a user with invalid email"""
        res = self.user.register("rodger", "rodger@mail.", "654123", "654123")
        self.assertEqual(res, "Username or email can only contain alphanumeric characters")

    def test_email_missing_at_sign(self):
        """Test registering a user with invalid email"""
        res = self.user.register("rodger", "rodgermail.com", "654123", "654123")
        self.assertEqual(res, "Username or email can only contain alphanumeric characters")

    def test_username_length(self):
        """Test registering a username with less than 3 characters"""
        res = self.user.register("rg", "rodger@mail.com", "654123", "654123")
        self.assertEqual(res, "username must be more than 3 characters")
        
    def test_existing_user_username(self):
        """Test with an already existing username, try registering a user twice"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        self.assertEqual(res, "Username or email already exists.")

    def test_existing_user_email(self):
        """Test registering a user with an existing email"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.register("rodgy", "rodger@mail.com", "654123", "654123")
        self.assertEqual(res, "Username or email already exists.")

    def test_password_length(self):
        """Test to ensure that a user has a strong password"""
        res = self.user.register("rodger", "rodger@mail.com", "654", "654")
        self.assertEqual(res, "Password too short")

    def test_password_match(self):
        """Test if password matching is working"""
        res = self.user.register("rodger", "rodger@mail.com", "654123", "1234654")
        self.assertEqual(res, "passwords do not match")
    
    def test_user_login(self):
        """Test if a user with valid details can login"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.login("rodger", "654123")
        self.assertEqual(res, "successful")

    def test_wrong_password(self):
        """Test for a login attempt with a wrong password"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.login("rodger", "65471234")
        self.assertEqual(res, "wrong password")

    def test_non_existing_user_login(self):
        """Test if a non-existing user can login"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.login("mzungu", "654123")
        self.assertEqual(res, "user does not exist")

    def test_find_user_by_id(self):
        """ Test if the method will find a user given a user id"""
        #first register a user and get their id
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        user_id = self.user.user_list[0]['id']
        res = self.user.find_user_by_id(user_id)
        #test if it retuens a dictionery with user details 
        self.assertIsInstance(res, dict)
        #test if the username of the returned user is the one registered
        username = res['username']
        self.assertIs(username, "rodger")
