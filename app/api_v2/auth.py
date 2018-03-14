import re
from flask import request, jsonify, g, url_for, render_template
from app.models import User, BlacklistToken
from app.email import send_mail
from . import api
from app import db

@api.before_app_request
def before_request():
    """get the user bafore every request"""
    if request.endpoint and 'auth' not in request.url:
        auth_header = request.headers.get('Authorization')
        g.user = None
        if auth_header:
            access_token = auth_header.split(" ")[1]
            if access_token:
                #try decoding the token and get the user_id
                res = User.decode_auth_token(access_token)
                if isinstance(res, int) and not BlacklistToken.is_blacklisted(access_token):
                    #check if no error in string format was returned
                    #find the user with the id on the token
                    user = User.query.filter_by(id=res).first()
                    g.user = user
                    return
                return jsonify({"message" : "Please register or login to continue"}), 401
            return jsonify({"message" : "acess token is missing"}), 401
        return jsonify({"message" : "Authorization header is missing"}), 401

def validdate_data(data):
    """validate user details"""
    try:
        #check if there are specil characters in the username
        if not re.match("^[a-zA-Z0-9_]*$", data['username'].strip()):
            return "username  can only contain alphanumeric characters"
        #check if the username is more than 3 characters
        elif len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        #check if the name contains only numbers or underscore
        elif not re.match("[a-zA-Z]{3,}_*[0-9_]*[a-zA-Z]*_*", data['username'].strip()):
            return "username must have atleast 3 letters before number or underscore"
        elif not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data['email'].strip()):
            return "please provide a valid email"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

def validate_password(data):
    """validate the password and return appropriate response"""
    try:
        #chack for spaces in password
        if " " in data["password"]:
            return "password should be one word, no spaces"
        elif len(data['password'].strip()) < 6:
            return "Password should have atleast 6 characters"
        #check if the passwords mact
        elif  data['password'] != data['cnfpassword']:
            return "passwords do not match"
        else:
            return "valid"
    #some data is missing and a keyError exception was raised
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@api.route('/auth/register', methods=['POST'])
def register():
    """ a route to register a user"""
    data = request.get_json()
    #validate the data
    res = validdate_data(data)
    check_pass = validate_password(data)
    if res is not "valid":
        return jsonify({"message" : res}), 400
    elif check_pass is not "valid":
        return jsonify({"message" : check_pass}), 400
    else:
        #all the deatails are valid, register the user
        user = User.query.filter((User.email==data['email']) | (User.username==data['username'])).first()
        if not user:
            #if no user with matching email
            try:
                username = data['username']
                email = data['email']
                password = data['password']
                user = User(username=username, email=email, password=password)
                user.save()

                #registration was successful
                response = {'message' : "registration successful, now login"}
                return jsonify(response), 201
            except Exception as error:
                #an error occured when trying to register the user
                response = {'message' : str(error)}
                return jsonify(response), 401
        else:
            # there is an existing user with given email
            response = {'message' : 'email or username exists, please login or chose another username'}
            return jsonify(response), 202

@api.route('/auth/login', methods=['POST'])
def login():
    """a route to handle user login and access token generation"""
    data = request.get_json()
    try:
        user = User.query.filter_by(username=data['username']).first()

        #verify found user details
        if user and user.verify_password(data['password']):
            #user details are valid hence generate the access token
            access_token = user.generate_auth_token()
            response = {
                    'message': 'login successful.',
                    'access_token':  access_token.decode()
            }
            return jsonify(response), 200
        else:
            #no user found, return an error message
            response = {'message': 'invalid username or password, Please try again'}
            return jsonify(response), 401
    except Exception as e:
        #an error occured in the server
        response = {'message': str(e)}
        return jsonify(response), 500

@api.route('/auth/gettoken', methods=['post'])
def get_token():
    """get the user email, generate a reset password token if user exists"""
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = user.generate_confirmation_token()
        subject = "Bright Events"
        confirm_url = url_for(
        'api.confirm_email',
        token=token,
        _external=True)
        html = render_template(
        'mail/reset_pass.html',
        confirm_url=confirm_url)
        send_mail(to=user.email, subject=subject, html=html)
        return jsonify({"message":"a confirmation email has been sent to {}".format(user.email),
                "token" : token.decode()}), 200
    return jsonify({"message" : "user not found, check the email and try again"}), 404

@api.route('/auth/confirm/<token>')
def confirm_email(token):
    """check if the confirmation token is  valid"""
    res = User.decode_confirmation_token(token)
    if res == "invalid or expired token":
        return jsonify({"message" : res}), 403
    #the token is valid.the user can now reset the password.
    #the token will also have to be passed along to the reset password form
    return jsonify({"message" : "confirmed, now reset your password"}), 200

@api.route('/auth/resetpass', methods=['PUT'])
def reset_pass():
    """confirm the user token and reset the password"""
    data = request.get_json()
    try:
        token = data['token']
    except KeyError:
        return jsonify({"message" : "please verify your email before resetting password"}), 401
    res = User.decode_confirmation_token(token)
    if res == "invalid or expired token":
        return jsonify({"message" : res}), 403
    #the token is valid and the response is a user object
    user = res
    #validate the given password
    check_pass = validate_password(data)
    if check_pass is not "valid":
        return jsonify({"message" : check_pass}), 400
    #the password is valid, thus reset the user password
    user.password = data["password"]
    user.save()
    return jsonify({"message" : "password reset successful, login"}), 200

@api.route('/auth/logout')
def logout():
    """store the access_token in blacklist when a user logs out"""
    auth_header= request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    #check is the token is valid
    res = User.decode_auth_token(access_token)
    if isinstance(res, int) and not BlacklistToken.is_blacklisted(access_token):
        #the token is still valid and not in blasklist
        blasklisted_token = BlacklistToken(access_token)
        db.session.add(blasklisted_token)
        db.session.commit()
        return jsonify({"message" : "logout succees. Thank you for using Bright Events"}), 200
    return jsonify({"message" : "you are already logged out"}), 401

