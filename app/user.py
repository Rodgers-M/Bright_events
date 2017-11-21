#to be used to match strings
import re


class User_details(object):
    """ A class to handle activities related to a user"""
    def __init__(self):

        # A list to hold all user objects
        self.user_list = []

    def register(self, username, password, cnfpassword):

        # empty dict to hold dgtails of the user to be created
        user_details = {}
        # checkif a user with that username exists
        for user in self.user_list:
            if username == user['username']:
                return "Username already exists."
        #validate password and username
        else:
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
                self.user_list.append(user_details)
                return "Registration successfull"

    def login(self, username, password):
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return "successful"
                else:
                    return "wrong password"
        return "user does not exist"
        