#used to validate names
import re


class User_details(object):
    """ A class to handle activities related to a user"""
    def __init__(self):

        # A list to hold all user objects
        self.user_list = []

    def register(self, username, password, cnfpassword):
        """A method to register users with correct and valid details"""

        # empty dict to hold dgtails of the user to be created
        user_details = {}
        # checkif a user with that username exists
        for user in self.user_list:
            if username == user['username']:
                return "Username already exists."
        else:
            #validate password and username
            if not re.match("^[a-zA-Z0-9_]*$", username):
                return "Username can only contain alphanumeric characters"
            elif password != cnfpassword:
                return "passwords do not match"
            elif len(password) < 6:
                return "Password too short"     
            else:
                #register user if all the details are valid
                user_details['username'] = username
                user_details['password'] = password
                user_details['id'] = len(self.user_list) + 1
                self.user_list.append(user_details)
                return "Registration successfull"

    def login(self, username, password):
        """A method to register a user given valid user details"""
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return "successful"
                else:
                    return "wrong password"
        return "user does not exist"
        