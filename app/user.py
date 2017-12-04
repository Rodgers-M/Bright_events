"""This module defines a user class and methods associated to it"""
#used to validate names
import re
import uuid


class User_details(object):
    """ A class to handle activities related to a user"""
    def __init__(self):
        # A list to hold all user objects
        self.user_list = []

    def register(self, username, email, password, cnfpassword):
        """A method to register users with correct and valid details"""

        # empty dict to hold dgtails of the user to be created
        user_details = {}
        # checkif a user with that username exists
        for user in self.user_list:
            if username == user['username']:
                return "Username already exists."
                break
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
                user_details['email'] = email
                user_details['password'] = password
                user_details['id'] = uuid.uuid1()
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
                    break
        return "user does not exist"

    def find_user_by_id(self, user_id):
        """ Retrieve a user given a user id"""
        for user in self.user_list:
            if user['id'] == user_id:
                return user
                break

    def reset_pass(self, username, newpass):
        """A method to reset a password"""
        for user in self.user_list:
            if user['username'] == username:
                user['password'] = newpass
                return "success"
                break
            return "incorrect username"