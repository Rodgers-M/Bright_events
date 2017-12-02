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
        res = self.user.register("rodger", "rodger@mail.com","654123", "654123")
        self.assertEqual(res, "Registration successfull")

    def test_existing_user(self):
        """TTest with an already existing user, try registering a user twice"""
        self.user.register("rodger", "rodger@mail.com", "654123", "654123")
        res = self.user.register("rodger", "rodger@mail.com","654123", "654123")
        self.assertEqual(res, "Username already exists.")

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
        self.user.register("rodger", "rodger@mail.com","654123", "654123")
        user_id = self.user.user_list[0]['id']
        res = self.user.find_user_by_id(user_id)
        #test if it retuens a dictionery with user details 
        self.assertIsInstance(res, dict)
        #test if the username of the returned user is the one registered
        username = res['username']
        self.assertIs(username, "rodger")



    
